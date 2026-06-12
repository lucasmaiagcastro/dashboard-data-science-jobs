"""Página de mercado — perfil das empresas contratantes."""
import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc

import src.charts as charts
import src.preprocessing as prep
from src.data import df, skills_df

dash.register_page(__name__, path="/mercado", name="Mercado")

SENIORITY_OPTIONS = [
    {"label": "Junior", "value": "junior"},
    {"label": "Pleno", "value": "midlevel"},
    {"label": "Senior", "value": "senior"},
    {"label": "Lead", "value": "lead"},
]
INDUSTRY_OPTIONS = prep.get_industry_options(df)

CARD_STYLE = {"background": "#1e293b", "borderRadius": "12px"}


def chart_card(graph_id):
    return dbc.Card(
        dbc.CardBody(dcc.Graph(id=graph_id, config={"displayModeBar": False})),
        className="border-0 shadow-sm h-100",
        style=CARD_STYLE,
    )


layout = html.Div([
    html.Div([
        html.H2("Empresas e Mercado", className="fw-bold mb-1"),
        html.P("Perfil das empresas que contratam profissionais de Ciência de Dados", className="text-muted mb-0", style={"fontSize": "14px"}),
    ], className="mb-4"),

    # Filters
    dbc.Card(
        dbc.CardBody(
            dbc.Row([
                dbc.Col([
                    dbc.Label("Indústria", className="text-muted", style={"fontSize": "12px"}),
                    dcc.Dropdown(id="mkt-filter-industry", options=INDUSTRY_OPTIONS, multi=True, placeholder="Todas as indústrias..."),
                ], md=6),
                dbc.Col([
                    dbc.Label("Senioridade", className="text-muted", style={"fontSize": "12px"}),
                    dcc.Dropdown(id="mkt-filter-seniority", options=SENIORITY_OPTIONS, multi=True, placeholder="Todos os níveis..."),
                ], md=6),
            ], className="g-3")
        ),
        className="border-0 mb-4 filter-card",
        style=CARD_STYLE,
    ),

    # Row 1: Tipo de empresa + Skills por senioridade
    dbc.Row([
        dbc.Col(chart_card("mkt-chart-ownership"), md=5),
        dbc.Col(chart_card("mkt-chart-skills-seniority"), md=7),
    ], className="mb-4 g-3"),

    # Row 2: Tamanho de empresa
    dbc.Row(
        dbc.Col(chart_card("mkt-chart-size")),
        className="mb-4",
    ),
])


@callback(
    [
        dash.Output("mkt-chart-ownership", "figure"),
        dash.Output("mkt-chart-skills-seniority", "figure"),
        dash.Output("mkt-chart-size", "figure"),
    ],
    [
        dash.Input("mkt-filter-industry", "value"),
        dash.Input("mkt-filter-seniority", "value"),
    ],
)
def update_market(industry, seniority):
    """Callback de mercado: capital, tamanho e skills médias por senioridade."""
    dff, _ = prep.apply_filters(df, skills_df, seniority=seniority, industry=industry)
    return (
        charts.make_ownership_chart(dff),
        charts.make_avg_skills_by_seniority_chart(dff),
        charts.make_company_size_chart(dff),
    )
