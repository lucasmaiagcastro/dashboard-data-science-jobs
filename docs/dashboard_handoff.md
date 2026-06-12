# Dashboard Data Science Jobs - Resumo do Projeto e Handoff

## Objetivo do Projeto

Desenvolver um dashboard interativo utilizando Dash e Plotly para a disciplina de Visualização de Dados, apresentando uma análise do mercado de trabalho em Ciência de Dados em 2025.

O objetivo principal é explorar tendências de contratação, habilidades mais demandadas, senioridade, salários e características das empresas que estão contratando profissionais da área.

---

# Trabalho Realizado Até o Momento

## 1. Análise Exploratória dos Dados (EDA)

Foi realizada uma análise inicial da base para compreender sua estrutura e qualidade.

### Verificações realizadas

- Quantidade de registros e colunas
- Tipos de dados
- Valores ausentes
- Registros duplicados
- Distribuição das principais variáveis
- Estrutura da coluna de skills
- Estrutura da coluna salarial

### Resultados

- 944 registros
- 13 colunas originais
- 0 registros duplicados
- Poucos valores ausentes nas colunas principais
- Base adequada para construção do dashboard

---

## 2. Análise de Negócio

Foi realizada uma análise para identificar quais informações possuem maior valor para o dashboard.

### Principais descobertas

#### Distribuição dos cargos

A base é fortemente concentrada em vagas de:

- Data Scientist → aproximadamente 91%
- Machine Learning Engineer → aproximadamente 8%
- Outros cargos → participação muito pequena

### Conclusão

O dashboard deve ser apresentado como:

"Panorama do Mercado de Ciência de Dados em 2025"

e não como

"Panorama do Mercado de Dados"

pois a base não possui diversidade suficiente de cargos.

---

### Senioridade

Distribuição predominante:

- Senior
- Lead

Resultado:

- 79,03% das vagas são Senior ou Lead

Insight importante para destaque no dashboard.

---

### Skills Mais Demandadas

Principais tecnologias encontradas:

1. Python
2. Machine Learning
3. SQL
4. R
5. AWS

As skills representam o principal ativo analítico da base.

---

### Setores que Mais Contratam

Principais setores:

- Technology
- Finance
- Retail
- Healthcare

Esses setores devem receber destaque nas visualizações.

---

### Salários

A coluna salarial foi tratada e convertida para formato numérico.

Salário médio ajustado:

€126.181,93

Foram identificados e removidos outliers extremos acima de €500.000 para análises estatísticas.

---

# Preparação dos Dados

Foi realizado tratamento e enriquecimento da base.

## Tratamentos realizados

### Valores ausentes

Valores ausentes categóricos foram preenchidos com:

"Não informado"

---

### Skills

A coluna de skills foi transformada em lista.

Também foi criada uma versão explodida para permitir análises individuais por tecnologia.

---

### Salários

Foram criadas as colunas:

- salary_min
- salary_max
- salary_avg
- salary_avg_adjusted

---

### Colunas auxiliares

Foram criadas colunas para facilitar análises futuras:

- is_senior_or_lead
- is_remote
- is_data_scientist
- skills_count

---

# Arquivos Disponíveis

## Dataset Principal

Arquivo:

data/data_science_jobs_clean.csv

Utilização:

Base principal para construção do dashboard.

Contém:

- Dados das vagas
- Dados salariais tratados
- Colunas auxiliares
- Informações de empresas
- Informações de senioridade
- Informações de setor

Este deve ser o dataset principal utilizado pelo Dash.

---

## Dataset de Skills

Arquivo:

data/data_science_jobs_skills_clean.csv

Utilização:

Análises específicas de tecnologias e competências.

Contém:

Uma linha para cada skill associada a uma vaga.

Exemplo:

Vaga A → Python

Vaga A → SQL

Vaga A → AWS

Esse dataset facilita:

- Top Skills
- Skills por Senioridade
- Skills por Setor

---

# Sugestão de Estrutura do Dashboard

## Página 1 - Visão Geral do Mercado

KPIs:

- Total de vagas
- Total de empresas
- Total de skills únicas
- Salário médio ajustado

Gráficos:

- Distribuição por senioridade
- Distribuição por setor
- Distribuição por modalidade de trabalho

---

## Página 2 - Skills e Tecnologias

Gráficos sugeridos:

- Top 15 skills mais demandadas
- Skills por senioridade
- Skills por setor

Observação:

Esta deve ser a página principal do dashboard.

Foi a área mais rica identificada durante as análises.

---

## Página 3 - Salários

Gráficos sugeridos:

- Histograma salarial
- Boxplot salarial por senioridade
- Salário médio por setor

Utilizar:

salary_avg_adjusted

para evitar influência de outliers extremos.

---

## Página 4 - Empresas e Mercado

Gráficos sugeridos:

- Top empresas contratantes
- Top localizações
- Distribuição por tamanho da empresa

---

# Filtros Recomendados

Filtros globais:

- Senioridade
- Setor
- Modalidade de trabalho
- Tamanho da empresa

Esses filtros devem atualizar os gráficos dinamicamente.

---

# Arquitetura Recomendada

Estrutura sugerida:

src/

- data_loader.py
- charts.py
- layouts.py
- callbacks.py

pages/

- overview.py
- skills.py
- salaries.py
- market.py

---

# Status Atual do Projeto

Concluído:

- Estrutura inicial do projeto
- EDA
- Business Understanding
- Data Cleaning
- Geração dos datasets finais

Próxima etapa:

- Design do dashboard
- Implementação Dash
- Criação dos gráficos
- Desenvolvimento dos callbacks
- Deploy na Plotly Cloud

O projeto encontra-se pronto para iniciar a fase de desenvolvimento do dashboard.
