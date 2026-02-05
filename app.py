"""
Dashboard de Salários - Área de Dados
Melhorias aplicadas seguindo melhores práticas de Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# CONFIGURAÇÕES E CONSTANTES
# ============================================

st.set_page_config(
    page_title="Dashboard de Salários",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mapeamento ISO-3 para países
ISO3_MAP = {
    'US': 'USA', 'UK': 'GBR', 'BR': 'BRA', 'DE': 'DEU', 'IN': 'IND',
    'CA': 'CAN', 'FR': 'FRA', 'AU': 'AUS', 'ES': 'ESP', 'NL': 'NLD',
    'IT': 'ITA', 'PT': 'PRT', 'JP': 'JPN', 'SG': 'SGP', 'CH': 'CHE',
    'MX': 'MEX', 'AR': 'ARG', 'CO': 'COL', 'CL': 'CHL', 'IE': 'IRL',
    'SE': 'SWE', 'NO': 'NOR', 'DK': 'DNK', 'FI': 'FIN', 'PL': 'POL',
    'CZ': 'CZE', 'RU': 'RUS', 'TR': 'TUR', 'AE': 'ARE', 'IL': 'ISR',
    'NZ': 'NZL', 'ZA': 'ZAF', 'HK': 'HKG', 'TW': 'TWN', 'KR': 'KOR',
    'CN': 'CHN', 'PH': 'PHL', 'ID': 'IDN', 'TH': 'THA', 'MY': 'MYS',
    'AT': 'AUT', 'BE': 'BEL', 'GR': 'GRC', 'HU': 'HUN', 'LU': 'LUX'
}

# Coordenadas de países para o mapa
COUNTRY_COORDS = {
    'USA': {'lat': 37.0902, 'lon': -95.7129},
    'GBR': {'lat': 55.3781, 'lon': -3.4360},
    'BRA': {'lat': -14.2350, 'lon': -51.9253},
    'DEU': {'lat': 51.1657, 'lon': 10.4515},
    'IND': {'lat': 20.5937, 'lon': 78.9629},
    'CAN': {'lat': 56.1304, 'lon': -106.3468},
    'FRA': {'lat': 46.2276, 'lon': 2.2137},
    'AUS': {'lat': -25.2744, 'lon': 133.7751},
    'ESP': {'lat': 40.4637, 'lon': -3.7492},
    'NLD': {'lat': 52.1326, 'lon': 5.2913},
    'ITA': {'lat': 41.8719, 'lon': 12.5674},
    'PRT': {'lat': 39.3999, 'lon': -8.2245},
    'JPN': {'lat': 36.2048, 'lon': 138.2529},
    'SGP': {'lat': 1.3521, 'lon': 103.8198},
    'CHE': {'lat': 46.8182, 'lon': 8.2275},
    'MEX': {'lat': 23.6345, 'lon': -102.5528},
    'ARG': {'lat': -38.4161, 'lon': -63.6167},
    'COL': {'lat': 4.5709, 'lon': -74.2973},
    'CHL': {'lat': -35.6751, 'lon': -71.5430},
    'IRL': {'lat': 53.1424, 'lon': -7.6921},
    'SWE': {'lat': 60.1282, 'lon': 18.6435},
    'NOR': {'lat': 60.4720, 'lon': 8.4689},
    'DNK': {'lat': 56.2639, 'lon': 9.5018},
    'FIN': {'lat': 61.9241, 'lon': 25.7482},
    'POL': {'lat': 51.9194, 'lon': 19.1451},
    'CZE': {'lat': 49.8175, 'lon': 15.4730},
    'RUS': {'lat': 61.5240, 'lon': 105.3188},
    'TUR': {'lat': 38.9637, 'lon': 35.2433},
    'ARE': {'lat': 23.4241, 'lon': 53.8478},
    'ISR': {'lat': 31.0461, 'lon': 34.8516},
    'NZL': {'lat': -40.9006, 'lon': 174.8860},
    'ZAF': {'lat': -30.5595, 'lon': 22.9375},
    'HKG': {'lat': 22.3193, 'lon': 114.1694},
    'TWN': {'lat': 23.6978, 'lon': 120.9605},
    'KOR': {'lat': 35.9078, 'lon': 127.7669},
    'CHN': {'lat': 35.8617, 'lon': 104.1954},
    'PHL': {'lat': 12.8797, 'lon': 121.7740},
    'IDN': {'lat': -0.7893, 'lon': 113.9213},
    'THA': {'lat': 15.8700, 'lon': 100.9925},
    'MYS': {'lat': 4.2105, 'lon': 101.9758},
    'AUT': {'lat': 47.5162, 'lon': 14.5501},
    'BEL': {'lat': 50.5039, 'lon': 4.4699},
    'GRC': {'lat': 39.0742, 'lon': 21.8243},
    'HUN': {'lat': 47.1625, 'lon': 19.5033},
    'LUX': {'lat': 49.8153, 'lon': 6.1296},
}

# Estilo CSS para insights
INSIGHT_CSS = """
<div style="background-color: #1E293B; padding: 15px; border-radius: 8px; margin-top: 10px;">
    <h4 style="color: #F8FAFC; margin-top: 0;">{title}</h4>
    <p style="color: #CBD5E1;"><b>Objetivo:</b> {objective}</p>
    <p style="color: #CBD5E1;"><b>Principais Achados:</b> {findings}</p>
    <p style="color: #CBD5E1;"><b>{note_title}:</b> {note}</p>
</div>
"""

# ============================================
# FUNÇÕES DE CARREGAMENTO E CACHE
# ============================================

@st.cache_data
def load_data() -> pd.DataFrame:
    """Carrega os dados do CSV com cache."""
    return pd.read_csv('data/dados-imersao-final.csv')

@st.cache_data
def get_yearly_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula estatísticas anuais."""
    return df.groupby('ano')['usd'].agg(['mean', 'median', 'count']).reset_index()

@st.cache_data
def get_country_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula estatísticas por país."""
    stats = df.groupby('residencia')['usd'].agg(['mean', 'count']).reset_index()
    stats.columns = ['residencia', 'usd', 'count']
    return stats

# ============================================
# FUNÇÕES DE VISUALIZAÇÃO
# ============================================

def render_kpi_metrics(df: pd.DataFrame) -> None:
    """Renderiza os 4 KPIs principais."""
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Salário Médio", f"${df['usd'].mean():,.0f}")
    col2.metric("Salário Máximo", f"${df['usd'].max():,.0f}")
    col3.metric("Mediana", f"${df['usd'].median():,.0f}")
    col4.metric("Registros", f"{len(df):,}")

def render_top_cargos(df: pd.DataFrame) -> None:
    """Renderiza gráfico de top 10 cargos."""
    top_cargos = df.groupby('cargo')['usd'].mean().nlargest(10).reset_index()
    fig = px.bar(
        top_cargos,
        x='usd',
        y='cargo',
        orientation='h',
        title="Top 10 Cargos com Maior Salário",
        color='usd',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        template="plotly_dark",
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(
        INSIGHT_CSS.format(
            title="Top 10 Cargos com Maior Salário",
            objective="Identificar os cargos mais bem remunerados na área de dados.",
            findings="Cargos técnicos como Machine Learning Engineer e Data Scientist lideram os salários.",
            note_title="Recomendação",
            note="Profissionais que buscam maximizar ganhos devem investir em habilidades de engenharia e ciência de dados."
        ),
        unsafe_allow_html=True
    )

def render_salary_distribution(df: pd.DataFrame) -> None:
    """Renderiza histograma com box plot."""
    fig = px.histogram(
        df,
        x='usd',
        nbins=40,
        title="Distribuição dos Salários",
        marginal="box"
    )
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(
        INSIGHT_CSS.format(
            title="Distribuição dos Salários",
            objective="Visualizar a concentração e variação dos salários.",
            findings="A distribuição é assimétrica à direita. A mediana é mais representativa do salário típico.",
            note_title="Interpretação",
            note="O box plot mostra mediana, quartis e outliers. Pontos isolados indicam exceções."
        ),
        unsafe_allow_html=True
    )

def render_yearly_trend(df: pd.DataFrame) -> None:
    """Renderiza gráfico de tendência anual."""
    yearly = get_yearly_stats(df)
    fig = px.line(
        yearly,
        x='ano',
        y='mean',
        title="Evolução Salarial Ano a Ano",
        markers=True
    )
    fig.update_traces(line_color='#6366F1', line_width=3)
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    yearly_min = yearly['ano'].min()
    yearly_max = yearly['ano'].max()
    growth = 0
    if yearly_min != yearly_max:
        growth = ((yearly.loc[yearly['ano'] == yearly_max, 'mean'].values[0] / 
                   yearly.loc[yearly['ano'] == yearly_min, 'mean'].values[0]) - 1) * 100
    
    st.markdown(
        INSIGHT_CSS.format(
            title="Evolução Salarial Ano a Ano",
            objective="Analisar a trajetória do mercado ao longo do tempo.",
            findings=f"De {yearly_min} a {yearly_max}, crescimento de {abs(growth):.1f}%.",
            note_title="Tendência",
            note="O mercado demonstra resiliência com tendência geral de crescimento."
        ),
        unsafe_allow_html=True
    )

def render_seniority_boxplot(df: pd.DataFrame) -> None:
    """Renderiza box plot por senioridade."""
    fig = px.box(
        df,
        x='senioridade',
        y='usd',
        color='senioridade',
        title="Distribuição por Senioridade"
    )
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    senior_mean = df.groupby('senioridade')['usd'].mean()
    jump = 0
    if 'Júnior' in senior_mean.index and 'Sênior' in senior_mean.index:
        jump = ((senior_mean['Sênior'] - senior_mean['Júnior']) / senior_mean['Júnior']) * 100
    
    st.markdown(
        INSIGHT_CSS.format(
            title="Distribuição por Senioridade",
            objective="Comparar remuneração entre níveis de experiência.",
            findings=f"A diferença Júnior → Sênior é de {jump:.0f}%.",
            note_title="Observação",
            note="A variabilidade aumenta com a senioridade, refletindo maior capacidade de negociação."
        ),
        unsafe_allow_html=True
    )

def render_country_map(df: pd.DataFrame) -> None:
    """Renderiza mapa coroplético por país."""
    country_stats = get_country_stats(df)
    country_stats['iso3'] = country_stats['residencia'].map(ISO3_MAP).fillna(country_stats['residencia'])
    country_stats['lat'] = country_stats['iso3'].map(lambda x: COUNTRY_COORDS.get(x, {}).get('lat'))
    country_stats['lon'] = country_stats['iso3'].map(lambda x: COUNTRY_COORDS.get(x, {}).get('lon'))
    country_with_coords = country_stats.dropna(subset=['lat', 'lon'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Choropleth(
        locations=country_stats['iso3'],
        z=country_stats['usd'],
        colorscale=[[0.0, '#1e3a5f'], [1.0, '#c9f0ff']],
        showscale=True,
        colorbar=dict(
            title='USD',
            tickprefix='$',
            tickformat=',.0f',
            len=0.6,
            thickness=15,
            bgcolor='rgba(30, 41, 59, 0.8)',
            titlefont={'color': '#F8FAFC'},
            tickfont={'color': '#F8FAFC'}
        ),
        marker_line_color='rgba(255,255,255,0.1)',
        hoverinfo='location+z'
    ))
    
    fig.add_trace(go.Scattergeo(
        lon=country_with_coords['lon'],
        lat=country_with_coords['lat'],
        text=country_with_coords['iso3'],
        mode='text',
        textfont=dict(family='Arial Black', size=11, color='white'),
        hoverinfo='text',
        hovertext=country_with_coords.apply(
            lambda r: f"<b>{r['residencia']}</b><br>${r['usd']:,.0f}<br>{r['count']} registros",
            axis=1
        )
    ))
    
    fig.update_layout(
        title={
            'text': 'Salário Médio por País',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#F8FAFC', 'family': 'Arial Black'}
        },
        geo=dict(
            projection_type='natural earth',
            showframe=False,
            showcoastlines=True,
            coastlinecolor='#64748b',
            showland=True,
            landcolor='#1e293b',
            showocean=True,
            oceancolor='#0f172a',
            showcountries=True,
            countrycolor='#334155',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=80, b=0),
        height=550
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    top_country = country_stats.loc[country_stats['usd'].idxmax()]
    
    st.markdown(
        INSIGHT_CSS.format(
            title="Salário Médio por País",
            objective="Comparar remuneração entre diferentes mercados geográficos.",
            findings=f"{top_country['residencia']} lidera com ${top_country['usd']:,.0f}. {len(country_stats)} países.",
            note_title="Consideração",
            note="Mercados europeus e asiáticos podem oferecer melhor custo-benefício considerando qualidade de vida."
        ),
        unsafe_allow_html=True
    )

def render_heatmap_seniority(df: pd.DataFrame) -> None:
    """Renderiza heatmap país × senioridade."""
    top_paises = df.groupby('residencia')['usd'].count().nlargest(15).index.tolist()
    heatmap_df = df[df['residencia'].isin(top_paises)].copy()
    heatmap_df['pais_iso3'] = heatmap_df['residencia'].map(ISO3_MAP).fillna(heatmap_df['residencia'])
    
    heatmap_data = heatmap_df.pivot_table(
        values='usd',
        index='pais_iso3',
        columns='senioridade',
        aggfunc='mean'
    ).fillna(0)
    
    def format_currency(x):
        if pd.isna(x) or x == 0:
            return "$0"
        if x >= 1000:
            return f"${x/1000:.0f}K"
        return f"${x:,.0f}"
    
    heatmap_text = heatmap_data.map(format_currency)
    
    fig = px.imshow(
        heatmap_data,
        aspect='auto',
        color_continuous_scale='Blues',
        title='Salário Médio por País e Senioridade'
    )
    fig.update_traces(text=heatmap_text.values, texttemplate="%{text}")
    fig.update_layout(
        template='plotly_dark',
        height=500,
        xaxis_title='Senioridade',
        yaxis_title='País (ISO-3)',
        coloraxis_colorbar=dict(title='USD', tickprefix='$', tickformat=',.0f')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    senior_cols = [c for c in heatmap_data.columns if c in df['senioridade'].unique()]
    senior_jump = 0
    if len(senior_cols) >= 2:
        avg_junior = heatmap_data[senior_cols[0]].mean()
        avg_senior = heatmap_data[senior_cols[-1]].mean()
        senior_jump = ((avg_senior - avg_junior) / avg_junior * 100) if avg_junior > 0 else 0
    
    st.markdown(
        INSIGHT_CSS.format(
            title="Salário por País e Senioridade",
            objective="Identificar onde cada nível é mais valorizado geograficamente.",
            findings=f"Progressão Júnior → {senior_cols[-1] if len(senior_cols) >= 2 else 'Sênior'}: +{senior_jump:.0f}%.",
            note_title="Estratégia",
            note="Considere mercados onde a diferença sênior-júnior é mais expressiva para maximizar renda."
        ),
        unsafe_allow_html=True
    )

def render_work_modality(df: pd.DataFrame) -> None:
    """Renderiza gráfico de modalidade de trabalho."""
    trabalho_stats = df.groupby('remoto')['usd'].mean().reset_index()
    trabalho_stats.columns = ['Tipo', 'Média']
    trabalho_stats = trabalho_stats.sort_values('Média', ascending=False)
    
    tipo_to_mean = dict(zip(trabalho_stats['Tipo'], trabalho_stats['Média']))
    
    fig = px.bar(
        trabalho_stats,
        x='Média',
        y='Tipo',
        orientation='h',
        text='Média',
        color='Média',
        color_continuous_scale=[(0, '#ef4444'), (0.5, '#f59e0b'), (1, '#22c55e')],
        title='Salário Médio por Tipo de Trabalho'
    )
    fig.update_traces(texttemplate='$%{x:,.0f}', textposition='outside')
    fig.update_layout(
        template='plotly_dark',
        height=400,
        yaxis_title=None,
        xaxis_title='Salário Médio (USD)',
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métricas de breakdown
    remote_mean = tipo_to_mean.get('Remoto')
    presencial_mean = tipo_to_mean.get('Presencial')
    hibrido_mean = tipo_to_mean.get('Híbrido')
    
    st.markdown("---")
    st.markdown("**Valores por modalidade:**")
    cols = st.columns(3)
    cols[0].metric("Remoto", f"${remote_mean:,.0f}" if remote_mean else "N/A")
    cols[1].metric("Presencial", f"${presencial_mean:,.0f}" if presencial_mean else "N/A")
    cols[2].metric("Híbrido", f"${hibrido_mean:,.0f}" if hibrido_mean else "N/A")
    
    # Insight comparativo
    if remote_mean and presencial_mean:
        diff_pct = ((remote_mean - presencial_mean) / presencial_mean) * 100
        if diff_pct > 0:
            st.success(f"Remoto ganha {diff_pct:.1f}% mais que Presencial")
        else:
            st.warning(f"Remoto ganha {abs(diff_pct):.1f}% menos que Presencial")
    
    remote_better = (remote_mean or 0) > (presencial_mean or 0)
    
    st.markdown(
        INSIGHT_CSS.format(
            title="Salário por Modalidade de Trabalho",
            objective="Analisar o impacto da modalidade na remuneração.",
            findings=f"{'Remoto' if remote_better else 'Presencial'} apresenta remuneração superior em média.",
            note_title="Cautela",
            note="A comparação pode ser influenciada por distribuição geográfica e mix de senioridade."
        ),
        unsafe_allow_html=True
    )

# ============================================
# MAIN APP
# ============================================

def main():
    with st.spinner('Carregando dados...'):
        df = load_data()
    
    st.title("💰 Dashboard de Salários")
    st.markdown("Análise salarial da área de dados (2020-2025)")
    
    # Sidebar com filtros
    with st.sidebar:
        st.header("Filtros")
        
        anos = sorted(df['ano'].unique())
        anos_sel = st.multiselect('Ano', anos, default=anos)
        
        senioridade = sorted(df['senioridade'].unique())
        senior_sel = st.multiselect('Senioridade', senioridade, default=senioridade)
        
        contrato = sorted(df['contrato'].unique())
        contrato_sel = st.multiselect('Contrato', contrato, default=contrato)
        
        tamanho = sorted(df['tamanho_empresa'].unique())
        tamanho_sel = st.multiselect('Tamanho', tamanho, default=tamanho)
        
        st.divider()
        st.caption(f"Total de registros: {len(df):,}")
    
    # Aplicar filtros
    df_filt = df[
        (df['ano'].isin(anos_sel)) &
        (df['senioridade'].isin(senior_sel)) &
        (df['contrato'].isin(contrato_sel)) &
        (df['tamanho_empresa'].isin(tamanho_sel))
    ]
    
    # KPIs
    render_kpi_metrics(df_filt)
    st.subheader("Visão Geral")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        render_top_cargos(df_filt)
    with col_g2:
        render_salary_distribution(df_filt)
    
    # Análises Avançadas
    with st.expander("Análises Avançadas", expanded=True):
        tab1, tab2, tab3, tab4 = st.tabs([
            "Tendência Anual",
            "Senioridade",
            "Países",
            "País × Modalidade"
        ])
        
        with tab1:
            render_yearly_trend(df_filt)
        
        with tab2:
            render_seniority_boxplot(df_filt)
        
        with tab3:
            render_country_map(df_filt)
        
        with tab4:
            col_h1, col_h2 = st.columns(2)
            with col_h1:
                render_heatmap_seniority(df_filt)
            with col_h2:
                render_work_modality(df_filt)
    
    # Dados detalhados
    st.divider()
    st.subheader("Dados Detalhados")
    
    col_d1, col_d2 = st.columns([3, 1])
    with col_d1:
        st.dataframe(df_filt, use_container_width=True)
    with col_d2:
        csv = df_filt.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Baixar CSV",
            csv,
            "salarios_filtrados.csv",
            "text/csv"
        )

if __name__ == "__main__":
    main()
