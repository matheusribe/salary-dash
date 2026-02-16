# Dashboard de Salários - Análise de Dados

## 📋 Sobre o Projeto

Este projeto apresenta uma análise completa de salários em posições relacionadas a dados (Data Science, Data Engineering, Analytics, etc.) através de um dashboard interativo que permite filtrar e visualizar informações por diferentes critérios como senioridade, tipo de contrato, localização e tamanho da empresa.

## 🚀 Tecnologias

- **Python 3.x**
- **Streamlit** - Framework web
- **Pandas** - Análise de dados
- **Plotly** - Visualizações interativas

## 📁 Estrutura

```
salary-dash/
├── app.py                      # Aplicação principal
├── .streamlit/
│   └── config.toml            # Configuração do tema
├── data/
│   └── dados-imersao-final.csv # Dataset
├── requirements.txt            # Dependências
└── README.md                  # Documentação
```

## ⚡ Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/salary-dash.git
cd salary-dash

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run app.py
```

Acesse em: `http://localhost:8501`

## 📊 Funcionalidades

### Filtros Interativos
- Ano (2020-2025)
- Senioridade (Júnior, Pleno, Sênior, Executivo)
- Tipo de Contrato
- Tamanho da Empresa

**Visão Geral:**
- Top 10 cargos com maior salário
- Distribuição dos salários (histograma + box plot)

**Análises Avançadas:**
- Evolução salarial ano a ano
- Distribuição por senioridade
- Mapa coroplético por país (com siglas ISO-3)
- Heatmap: País × Senioridade
- Comparação: Remoto vs Presencial vs Híbrido

### Insights
- **5.000+ registros** de salários em diferentes posições de dados
- Dados de **2020 a 2025**
- **50+ países** representados
- **100+ tipos** de cargos diferentes na área de dados

## 🎨 Tema

Tema escuro moderno (slate/indigo) configurado via `.streamlit/config.toml`.

## 📈 Dataset

- **5.000+ registros** de salários
- Período: **2020-2025**
- **50+ países** representados
- **100+ cargos** na área de dados

## 👤 Autor

Desenvolvido durante a Imersão Python da Alura

- GitHub: [@matheusribe](https://github.com/matheusribe)
- LinkedIn: [matheusribe](https://linkedin.com/in/matheusribe)

## 📝 Licença
---
Desenvolvido durante a **Imersão Python da Alura**

- **GitHub**: [matheusribe](https://github.com/matheusribe)
- **LinkedIn**: [matheusribe](https://linkedin.com/in/matheusribe)
---
MIT License
