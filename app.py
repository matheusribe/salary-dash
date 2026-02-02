import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Dashboard de Salários", 
    page_icon="📊",
    layout="wide"
 )

# Load data
df = pd.read_csv('data/dados-imersao-final.csv')

# Fidebar filters
st.sidebar.header("🔍 Filtros")

# Filter by year
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect('Ano', anos_disponiveis, default=anos_disponiveis)

# Filter by job level
senioridade_disponiveis = sorted(df['senioridade'].unique())
senioridade_selecionados = st.sidebar.multiselect('Nível de Senioridade', senioridade_disponiveis, default=senioridade_disponiveis)

# Filter by job type
constratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect('Tipo de Contrato', constratos_disponiveis, default=constratos_disponiveis)

# Filter by company size
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect('Tamanho da Empresa', tamanhos_disponiveis, default=tamanhos_disponiveis)

# Apply filters
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridade_selecionados)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# Main page
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros interativos a esquerda.")

# Main metrics
st.subheader("📈 Métricas Gerais (Salário anual em USD)") 
if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_medio = 0
    salario_maximo = 0
    total_registros = 0
    cargo_mais_frequente = "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio (USD)", f"${salario_medio:,.2f}")
col2.metric("Salário Máximo (USD)", f"${salario_maximo:,.2f}")
col3.metric("Total de Registros", total_registros)
col4.metric("Cargo Mais Frequente", cargo_mais_frequente)
st.markdown("---")

# Visualizations
st.subheader("Gráficos")
col_graf1, col_graf2 = st.columns(2)
with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos, 
            x='usd', 
            y='cargo', 
            orientation='h', 
            title='Top 10 Cargos com Maior Salário Médio',
            labels={'usd': 'Salário Médio (USD)', 'cargo': 'Cargo'}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado, 
            x='usd', 
            nbins=30, 
            title='Distribuição dos Salários', 
            labels={'usd': 'Salário (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem, 
            names='tipo_trabalho', 
            values='quantidade', 
            title='Proporção de Tipos de Trabalho',
            hole=0.5
        )

        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico.")

# Table view
st.subheader("📋 Dados Detalhados")
st.dataframe(df_filtrado)
