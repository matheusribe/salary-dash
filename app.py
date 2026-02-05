import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard de Salários",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    return pd.read_csv('data/dados-imersao-final.csv')

@st.cache_data
def get_top_cargos(df):
    return df.groupby('cargo')['usd'].mean().nlargest(10).reset_index()

@st.cache_data
def get_yearly_stats(df):
    return df.groupby('ano')['usd'].agg(['mean', 'median', 'count']).reset_index()

@st.cache_data
def get_country_avg(df):
    return df.groupby('pais')['usd'].mean().reset_index()

with st.spinner('🔄 Carregando dados...'):
    df = load_data()

st.title("💰 Dashboard de Salários")
st.markdown("Análise salarial da área de dados (2020-2025)")

with st.sidebar:
    st.header("🔍 Filtros")
    
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

df_filt = df[
    (df['ano'].isin(anos_sel)) &
    (df['senioridade'].isin(senior_sel)) &
    (df['contrato'].isin(contrato_sel)) &
    (df['tamanho_empresa'].isin(tamanho_sel))
]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio", f"${df_filt['usd'].mean():,.0f}")
col2.metric("Salário Máximo", f"${df_filt['usd'].max():,.0f}")
col3.metric("Mediana", f"${df_filt['usd'].median():,.0f}")
col4.metric("Registros", f"{len(df_filt):,}")

st.subheader("📊 Visão Geral")

col_g1, col_g2 = st.columns(2)

with col_g1:
    top_cargos = df_filt.groupby('cargo')['usd'].mean().nlargest(10).reset_index()
    fig1 = px.bar(
        top_cargos,
        x='usd',
        y='cargo',
        orientation='h',
        title="Top 10 Cargos com Maior Salário",
        color='usd',
        color_continuous_scale='Viridis'
    )
    fig1.update_layout(template="plotly_dark", height=400, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    fig2 = px.histogram(
        df_filt,
        x='usd',
        nbins=40,
        title="Distribuição dos Salários",
        marginal="box"
    )
    fig2.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig2, use_container_width=True)

with st.expander("📈 Análises Avançadas", expanded=True):
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Tendência Anual",
        "📦 Senioridade",
        "🌍 Países",
        "🏢 Hierarquia"
    ])
    
    with tab1:
        yearly = df_filt.groupby('ano')['usd'].agg(['mean', 'median', 'count']).reset_index()
        fig3 = px.line(
            yearly,
            x='ano',
            y='mean',
            title="Evolução Salarial Ano a Ano",
            markers=True
        )
        fig3.update_traces(line_color='#6366F1', line_width=3)
        fig3.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        fig4 = px.box(
            df_filt,
            x='senioridade',
            y='usd',
            color='senioridade',
            title="Distribuição por Senioridade"
        )
        fig4.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    with tab3:
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
            'DNK': {'lat': 56.2639, 'lon': 9.5018},
            'GRC': {'lat': 39.0742, 'lon': 21.8243},
            'HUN': {'lat': 47.1625, 'lon': 19.5033},
            'LUX': {'lat': 49.8153, 'lon': 6.1296},
        }

        iso3_map = {
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

        country_avg = df_filt.groupby('residencia')['usd'].agg(['mean', 'count']).reset_index()
        country_avg.columns = ['residencia', 'usd', 'count']
        country_avg['iso3'] = country_avg['residencia'].map(iso3_map).fillna(country_avg['residencia'])
        country_avg['lat'] = country_avg['iso3'].map(lambda x: COUNTRY_COORDS.get(x, {}).get('lat'))
        country_avg['lon'] = country_avg['iso3'].map(lambda x: COUNTRY_COORDS.get(x, {}).get('lon'))
        country_with_coords = country_avg.dropna(subset=['lat', 'lon'])

        fig5 = go.Figure()

        fig5.add_trace(go.Choropleth(
            locations=country_avg['iso3'],
            z=country_avg['usd'],
            colorscale=[
                [0.0, '#1e3a5f'],
                [0.2, '#2d5a87'],
                [0.4, '#3d7ab0'],
                [0.6, '#5ba0c8'],
                [0.8, '#8ec8e0'],
                [1.0, '#c9f0ff']
            ],
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

        fig5.add_trace(go.Scattergeo(
            lon=country_with_coords['lon'],
            lat=country_with_coords['lat'],
            text=country_with_coords['iso3'],
            mode='text',
            textfont=dict(
                family='Arial Black',
                size=11,
                color='white'
            ),
            hoverinfo='text',
            hovertext=country_with_coords.apply(
                lambda r: f"<b>{r['residencia']}</b><br>💰 ${r['usd']:,.0f}<br>📊 {r['count']} registros",
                axis=1
            )
        ))

        fig5.update_layout(
            title={
                'text': '💰 Salário Médio por País',
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

        st.plotly_chart(fig5, use_container_width=True)

    with tab4:
        sample = df_filt.sample(min(500, len(df_filt)))
        fig6 = px.sunburst(
            sample,
            path=['residencia', 'cargo', 'empresa'],
            values='usd',
            title="Hierarquia: País → Cargo → Empresa"
        )
        fig6.update_layout(template="plotly_dark", height=500)
        st.plotly_chart(fig6, use_container_width=True)

st.divider()
st.subheader("📋 Dados Detalhados")

col_d1, col_d2 = st.columns([3, 1])

with col_d1:
    st.dataframe(df_filt, use_container_width=True)

with col_d2:
    csv = df_filt.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Baixar CSV",
        csv,
        "salarios_filtrados.csv",
        "text/csv"
    )
