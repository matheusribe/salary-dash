# Dashboard de Salários — Análise de Dados com Python e Streamlit

Um dashboard interativo desenvolvido em Streamlit para análise e visualização de salários na área de dados.

## 📋 Sobre o Projeto

Este projeto apresenta uma análise completa de salários em posições relacionadas a dados (Data Science, Data Engineering, Analytics, etc.) através de um dashboard interativo que permite filtrar e visualizar informações por diferentes critérios como senioridade, tipo de contrato, localização e tamanho da empresa.

## 🚀 Tecnologias Utilizadas

- **Python 3.x**
- **Streamlit** - Framework para criação do dashboard web
- **Pandas** - Manipulação e análise de dados
- **Plotly Express** - Visualizações interativas
- **Jupyter Notebook** - Desenvolvimento e análise exploratória

## 📁 Estrutura do Projeto

```
├── app.py                                    # Aplicação Streamlit principal
├── data/
│   └── dados-imersao-final.csv              # Dataset tratado e limpo
├── nb/
│   └── 2026_Imersão_dados_com_Python_Alura.ipynb  # Notebook com análise exploratória
├── requirements.txt                          # Dependências do projeto
└── README.md                                # Documentação
```

## 🔧 Como Executar o Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/dashboard-salarios-dados.git
cd dashboard-salarios-dados
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação
```bash
streamlit run app.py
```

O dashboard estará disponível em `http://localhost:8501`

## 📊 Funcionalidades

### Filtros Interativos
- **Ano**: Seleção de período temporal
- **Nível de Senioridade**: Júnior, Pleno, Sênior, Executivo
- **Tipo de Contrato**: Tempo Integral, Contrato, Meio Período, Freelancer
- **Tamanho da Empresa**: Pequeno, Médio, Grande

### Métricas Principais
- Salário médio anual em USD
- Salário máximo registrado
- Total de registros filtrados
- Cargo mais frequente

### Visualizações
1. **Gráfico de Barras Horizontais**: Top 10 cargos com maior salário médio
2. **Histograma**: Distribuição dos salários
3. **Gráfico Pizza**: Proporção de tipos de trabalho (Presencial/Remoto/Híbrido)
4. **Mapa Coroplético**: Salário médio de Data Scientists por país

### Tabela Interativa
Visualização completa dos dados filtrados com opções de busca e ordenação.

## 📈 Insights do Dataset

- **5.000+ registros** de salários em diferentes posições de dados
- Dados de **2020 a 2025**
- **50+ países** representados
- **100+ tipos** de cargos diferentes na área de dados

## 🛠️ Desenvolvimento

### Processo de Limpeza dos Dados

O notebook `2026_Imersão_dados_com_Python_Alura.ipynb` contém todo o processo de:

1. **Importação e Exploração**: Carregamento do dataset original
2. **Tradução**: Conversão de colunas para português
3. **Limpeza**: Tratamento de valores nulos e inconsistências
4. **Transformação**: Conversão de códigos para valores legíveis
5. **Validação**: Verificação da qualidade dos dados

### Estrutura do Código

- `app.py`: Aplicação principal do Streamlit com interface e visualizações
- Carregamento de dados via `pd.read_csv('data/dados-imersao-final.csv')`
- Filtros implementados através de widgets do Streamlit
- Gráficos gerados dinamicamente com Plotly Express

## 👥 Autor

Desenvolvido durante a **Imersão Python da Alura**

- **GitHub**: [matheusribe](https://github.com/matheusribe)
- **LinkedIn**: [matheusribe](https://linkedin.com/in/matheusribe)

