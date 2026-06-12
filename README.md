# Dashboard de Vagas em Ciência de Dados

Dashboard interativo para análise do mercado de trabalho em **Ciência de Dados em 2025**, desenvolvido para a disciplina de **Visualização de Dados** da **Unichristus**.

**Participantes:** Lucas Maia e Gustavo Távora

O projeto transforma uma base de ~944 vagas em visualizações exploratórias sobre senioridade, skills, salários, setores e perfil das empresas contratantes — com filtros dinâmicos que atualizam todos os gráficos em tempo real.

---

## Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Principais insights](#principais-insights)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Callbacks e interatividade](#callbacks-e-interatividade)
- [Dados](#dados)
- [Como executar](#como-executar)
- [Deploy](#deploy)
- [Notebooks e pipeline de dados](#notebooks-e-pipeline-de-dados)
- [Licença](#licença)

---

## Sobre o projeto

O mercado de Ciência de Dados cresce rapidamente, mas entender **o que as empresas exigem**, **quanto pagam** e **de onde vêm as oportunidades** exige ir além de tabelas estáticas. Este dashboard responde a essas perguntas por meio de quatro páginas temáticas, cada uma focada em um recorte analítico do mercado.

A base concentra-se predominantemente em vagas de **Data Scientist** (~91%) e **Machine Learning Engineer** (~8%), com forte presença de posições **Senior** e **Lead** (~79%). Por isso, o escopo do dashboard é apresentado como:

> **Panorama do Mercado de Ciência de Dados em 2025**

e não como um panorama genérico de "mercado de dados".

---

## Principais insights

| Dimensão | Destaque |
|---|---|
| **Cargos** | ~91% Data Scientist, ~8% ML Engineer |
| **Senioridade** | ~79% das vagas são Senior ou Lead |
| **Skills** | Python, Machine Learning, SQL, R e AWS lideram a demanda |
| **Setores** | Tecnologia, Finanças, Varejo e Saúde concentram a maior parte das vagas |
| **Salário médio** | ~€126.182 (ajustado, sem outliers acima de €500k) |

---

## Funcionalidades

### Visão Geral (`/`)

Panorama macro do mercado com KPIs e distribuições:

- **KPIs:** total de vagas, empresas únicas, skills únicas e salário médio ajustado
- **Gráficos:** distribuição por senioridade, modalidade de trabalho (presencial/híbrido/remoto) e indústria
- **Filtros:** senioridade, modalidade e indústria

### Skills (`/skills`)

Página central do dashboard — a área mais rica da base:

- **Top 15 skills** mais demandadas (gráfico de barras horizontal)
- **Heatmap** de skills por senioridade
- **Heatmap** de skills por indústria
- **Filtros:** senioridade e indústria

### Salários (`/salarios`)

Análise da remuneração com foco em comparações:

- **Histograma** da distribuição salarial
- **Boxplot** salarial por senioridade
- **Boxplot** salarial por indústria
- **Salário mediano** por skill (top 12)
- **Filtros:** senioridade, modalidade e indústria
- Utiliza `salary_avg_adjusted` para mitigar outliers extremos

### Mercado (`/mercado`)

Perfil das empresas contratantes:

- **Distribuição** por tipo de capital (aberto/fechado)
- **Média de skills exigidas** por senioridade
- **Distribuição** por tamanho da empresa (pequena → muito grande)
- **Filtros:** indústria e senioridade

Todos os gráficos respondem aos filtros selecionados via callbacks Dash e exibem estado vazio quando não há dados para a combinação escolhida.

---

## Callbacks e interatividade

A interatividade do dashboard é implementada com **callbacks do Dash** — funções Python decoradas com `@callback` que conectam **Inputs** (filtros) a **Outputs** (KPIs e gráficos). Cada página em `pages/` possui seu próprio callback, isolado das demais.

### Fluxo de um callback

```
Dropdown (Input) → apply_filters() → charts.make_*() → dcc.Graph (Output)
```

1. O usuário altera um filtro (`dcc.Dropdown`)
2. O Dash dispara o callback da página com os valores selecionados
3. `prep.apply_filters()` filtra `df` e `skills_df` conforme senioridade, modalidade e/ou indústria
4. As funções em `src/charts.py` geram novas figuras Plotly com os dados filtrados
5. Os gráficos e KPIs são atualizados na tela sem recarregar a página

### Callbacks por página

| Página | Arquivo | Inputs | Outputs |
|---|---|---|---|
| Visão Geral | `pages/overview.py` | senioridade, modalidade, indústria | 4 KPIs + 3 gráficos |
| Skills | `pages/skills.py` | senioridade, indústria | 3 gráficos |
| Salários | `pages/salaries.py` | senioridade, modalidade, indústria | 4 gráficos |
| Mercado | `pages/market.py` | indústria, senioridade | 3 gráficos |

### Exemplo — página de Salários

```python
@callback(
    [
        dash.Output("sal-chart-histogram", "figure"),
        dash.Output("sal-chart-boxplot-seniority", "figure"),
        dash.Output("sal-chart-industry", "figure"),
        dash.Output("sal-chart-skill", "figure"),
    ],
    [
        dash.Input("sal-filter-seniority", "value"),
        dash.Input("sal-filter-status", "value"),
        dash.Input("sal-filter-industry", "value"),
    ],
)
def update_salaries(seniority, status, industry):
    dff, dff_skills = prep.apply_filters(df, skills_df, seniority, status, industry)
    return (
        charts.make_salary_histogram(dff),
        charts.make_salary_boxplot_by_seniority(dff),
        charts.make_salary_by_industry_chart(dff),
        charts.make_salary_by_skill_chart(dff_skills),
    )
```

Quando nenhum registro corresponde aos filtros, `src/charts.py` retorna um gráfico vazio com a mensagem *"Sem dados para os filtros selecionados"*.

O app usa `suppress_callback_exceptions=True` em `app.py` para permitir callbacks definidos em páginas que ainda não foram carregadas pelo roteamento multi-page do Dash.

---

## Tecnologias

| Camada | Ferramenta |
|---|---|
| Linguagem | Python 3 |
| Framework web | [Dash](https://dash.plotly.com/) (multi-page) |
| Visualizações | [Plotly](https://plotly.com/python/) |
| UI / layout | [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) (tema Darkly) |
| Manipulação de dados | [Pandas](https://pandas.pydata.org/) |
| Análise exploratória | Matplotlib, Seaborn (notebooks) |
| Deploy | [Plotly Cloud](https://plotly.com/cloud/) |

---

## Estrutura do repositório

```
dashboard-data-science-jobs/
├── app.py                  # Entry point — navbar, layout global e servidor WSGI
├── requirements.txt        # Dependências Python
├── assets/
│   └── style.css           # Estilos customizados (tema escuro, fonte Inter)
├── data/
│   ├── data_science_job_posts_2025.csv   # Dataset bruto original
│   ├── data_science_jobs_clean.csv       # Dataset principal tratado (944 vagas)
│   └── data_science_jobs_skills_clean.csv # Skills explodidas (1 linha por skill/vaga)
├── docs/
│   └── dashboard_handoff.md              # Documentação de handoff e decisões analíticas
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_business_understanding.ipynb
│   └── 03_data_cleaning_and_preparation.ipynb
├── pages/
│   ├── overview.py         # Página: Visão Geral
│   ├── skills.py           # Página: Skills e Tecnologias
│   ├── salaries.py         # Página: Análise Salarial
│   └── market.py           # Página: Empresas e Mercado
└── src/
    ├── data.py             # Carrega os CSVs na inicialização do app
    ├── preprocessing.py    # Filtros, KPIs e agregações
    └── charts.py           # Funções Plotly para cada visualização
```

### Arquitetura

```
CSV (data/) → preprocessing.py → charts.py → pages/ (callbacks) → app.py
                     ↑
                 data.py (load na startup)
```

- **`src/data.py`** — carrega os datasets uma única vez na inicialização
- **`src/preprocessing.py`** — lógica de negócio: filtros, labels em português, agregações e KPIs
- **`src/charts.py`** — factory de gráficos Plotly com paleta e layout consistentes
- **`pages/`** — uma página Dash por módulo analítico, com layout e callbacks isolados

---

## Dados

### Origem

A base original (`data_science_job_posts_2025.csv`) contém **944 registros** e **13 colunas**, sem duplicatas e com poucos valores ausentes nas colunas principais.

### Tratamentos aplicados

Os notebooks em `notebooks/` documentam todo o pipeline. Resumo das transformações:

| Etapa | Descrição |
|---|---|
| Valores ausentes | Preenchidos com `"Não informado"` em colunas categóricas |
| Skills | Convertidas em lista; gerada versão explodida (1 linha/skill) |
| Salários | Parsing de faixas → `salary_min`, `salary_max`, `salary_avg`, `salary_avg_adjusted` |
| Outliers | Removidos valores acima de €500.000 para análises estatísticas |
| Colunas auxiliares | `is_senior_or_lead`, `is_remote`, `is_data_scientist`, `skills_count` |

### Colunas do dataset principal

| Coluna | Descrição |
|---|---|
| `job_title` | Título da vaga |
| `seniority_level` | Nível: junior, midlevel, senior, lead |
| `status` | Modalidade: on-site, hybrid, remote |
| `company` | Nome da empresa |
| `location` | Local da vaga |
| `headquarter` | Sede da empresa |
| `industry` | Setor (Technology, Finance, Retail, Healthcare, …) |
| `ownership` | Tipo de capital (Public, Private) |
| `company_size` | Tamanho da empresa |
| `salary_avg_adjusted` | Salário médio ajustado (€) |
| `skills_list` | Lista de skills exigidas |
| `skills_count` | Quantidade de skills na vaga |

### Dataset de skills

`data_science_jobs_skills_clean.csv` contém **~4.181 linhas** — uma por combinação vaga/skill — e é usado para análises de frequência, heatmaps e salário por tecnologia.

---

## Como executar

### Pré-requisitos

- Python 3.10+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/<seu-usuario>/dashboard-data-science-jobs.git
cd dashboard-data-science-jobs

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Executar localmente

```bash
python app.py
```

Acesse **http://127.0.0.1:8050** no navegador. O servidor inicia em modo debug por padrão.

---

## Deploy

O dashboard está configurado para publicação na **Plotly Cloud**. O arquivo `plotly-cloud.v4.toml` contém a configuração da aplicação publicada.

Para fazer deploy de uma nova versão, consulte a [documentação oficial do Plotly Cloud](https://plotly.com/cloud/deploy/).

---

## Notebooks e pipeline de dados

A análise que fundamenta o dashboard está documentada em três notebooks Jupyter:

| Notebook | Conteúdo |
|---|---|
| `01_exploratory_data_analysis.ipynb` | EDA: estrutura, qualidade, distribuições e valores ausentes |
| `02_business_understanding.ipynb` | Definição de perguntas de negócio e insights para o dashboard |
| `03_data_cleaning_and_preparation.ipynb` | Tratamento, enriquecimento e exportação dos CSVs finais |

Documentação complementar de decisões analíticas e handoff: [`docs/dashboard_handoff.md`](docs/dashboard_handoff.md).

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE) — Copyright (c) 2026 Lucas Maia e Gustavo Távora.
