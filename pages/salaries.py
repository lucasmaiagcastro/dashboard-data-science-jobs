import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc

import src.charts as charts
import src.preprocessing as prep
from src.data import df, skills_df

dash.register_page(__name__, path="/salarios", name="Salários")

SENIORITY_OPTIONS = [
    {"label": "Junior", "value": "junior"},
    {"label": "Mid-level", "value": "midlevel"},
    {"label": "Senior", "value": "senior"},
    {"label": "Lead", "value": "lead"},
]
STATUS_OPTIONS = [
    {"label": "Presencial", "value": "on-site"},
    {"label": "Híbrido", "value": "hybrid"},
    {"label": "Remoto", "value": "remote"},
]
INDUSTRY_OPTIONS = [{"label": i, "value": i} for i in sorted(df["industry"].unique()) if i != "Não informado"]

CARD_STYLE = {"background": "#1e293b", "borderRadius": "12px"}


def chart_card(graph_id):
    return dbc.Card(
        dbc.CardBody(dcc.Graph(id=graph_id, config={"displayModeBar": False})),
        className="border-0 shadow-sm h-100",
        style=CARD_STYLE,
    )


layout = html.Div([
    html.Div([
        html.H2("Análise Salarial", className="fw-bold mb-1"),
        html.P("Distribuição e comparação de salários por senioridade, indústria e skill", className="text-muted mb-0", style={"fontSize": "14px"}),
    ], className="mb-4"),

    # Filters
    dbc.Card(
        dbc.CardBody(
            dbc.Row([
                dbc.Col([
                    dbc.Label("Senioridade", className="text-muted", style={"fontSize": "12px"}),
                    dcc.Dropdown(id="sal-filter-seniority", options=SENIORITY_OPTIONS, multi=True, placeholder="Todos os níveis..."),
                ], md=4),
                dbc.Col([
                    dbc.Label("Modalidade", className="text-muted", style={"fontSize": "12px"}),
                    dcc.Dropdown(id="sal-filter-status", options=STATUS_OPTIONS, multi=True, placeholder="Todas as modalidades..."),
                ], md=4),
                dbc.Col([
                    dbc.Label("Indústria", className="text-muted", style={"fontSize": "12px"}),
                    dcc.Dropdown(id="sal-filter-industry", options=INDUSTRY_OPTIONS, multi=True, placeholder="Todas as indústrias..."),
                ], md=4),
            ], className="g-3")
        ),
        className="border-0 mb-4 filter-card",
        style=CARD_STYLE,
    ),

    # Row 1: Histograma + Boxplot senioridade
    dbc.Row([
        dbc.Col(chart_card("sal-chart-histogram"), md=5),
        dbc.Col(chart_card("sal-chart-boxplot-seniority"), md=7),
    ], className="mb-4 g-3"),

    # Row 2: Boxplot indústria
    dbc.Row(
        dbc.Col(chart_card("sal-chart-industry")),
        className="mb-4",
    ),

    # Row 3: Salário por skill
    dbc.Row(
        dbc.Col(chart_card("sal-chart-skill")),
        className="mb-4",
    ),
])


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
