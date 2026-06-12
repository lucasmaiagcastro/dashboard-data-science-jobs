import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

import src.charts as charts
import src.preprocessing as prep
from src.data import df, skills_df

dash.register_page(__name__, path="/", name="Visão Geral")

SENIORITY_OPTIONS = [
    {"label": "Junior", "value": "junior"},
    {"label": "Pleno", "value": "midlevel"},
    {"label": "Senior", "value": "senior"},
    {"label": "Lead", "value": "lead"},
]
STATUS_OPTIONS = [
    {"label": "Presencial", "value": "on-site"},
    {"label": "Híbrido", "value": "hybrid"},
    {"label": "Remoto", "value": "remote"},
]
INDUSTRY_OPTIONS = prep.get_industry_options(df)

CARD_STYLE = {"background": "#1e293b", "borderRadius": "12px"}


def kpi_card(icon, label, value_id, color):
    return dbc.Card(
        dbc.CardBody(
            html.Div([
                html.Div(
                    html.I(className=f"bi {icon}", style={"fontSize": "1.6rem", "color": color}),
                    className="d-flex align-items-center justify-content-center rounded-3 p-2",
                    style={"background": f"{color}22", "width": "48px", "height": "48px"},
                ),
                html.Div([
                    html.P(label, className="text-muted mb-0", style={"fontSize": "12px"}),
                    html.H5(id=value_id, className="fw-bold mb-0", style={"color": color}),
                ], className="ms-3"),
            ], className="d-flex align-items-center")
        ),
        className="border-0 shadow-sm h-100",
        style=CARD_STYLE,
    )


def chart_card(graph_id):
    return dbc.Card(
        dbc.CardBody(dcc.Graph(id=graph_id, config={"displayModeBar": False})),
        className="border-0 shadow-sm h-100",
        style=CARD_STYLE,
    )


layout = html.Div([
    # Page title
    html.Div([
        html.H2("Visão Geral do Mercado", className="fw-bold mb-1"),
        html.P("Panorama do Mercado de Ciência de Dados em 2025", className="text-muted mb-0", style={"fontSize": "14px"}),
    ], className="mb-4"),

    # Filters
    dbc.Card(
        dbc.CardBody(
            dbc.Row([
                dbc.Col([
                    dbc.Label("Senioridade", className="text-muted", style={"fontSize": "12px"}),
                    dcc.Dropdown(id="ov-filter-seniority", options=SENIORITY_OPTIONS, multi=True, placeholder="Todos os níveis..."),
                ], md=4),
                dbc.Col([
                    dbc.Label("Modalidade", className="text-muted", style={"fontSize": "12px"}),
                    dcc.Dropdown(id="ov-filter-status", options=STATUS_OPTIONS, multi=True, placeholder="Todas as modalidades..."),
                ], md=4),
                dbc.Col([
                    dbc.Label("Indústria", className="text-muted", style={"fontSize": "12px"}),
                    dcc.Dropdown(id="ov-filter-industry", options=INDUSTRY_OPTIONS, multi=True, placeholder="Todas as indústrias..."),
                ], md=4),
            ], className="g-3")
        ),
        className="border-0 mb-4 filter-card",
        style=CARD_STYLE,
    ),

    # KPIs
    dbc.Row([
        dbc.Col(kpi_card("bi-briefcase-fill", "Total de Vagas", "ov-kpi-jobs", "#6366f1"), md=3),
        dbc.Col(kpi_card("bi-building-fill", "Empresas", "ov-kpi-companies", "#06b6d4"), md=3),
        dbc.Col(kpi_card("bi-lightning-fill", "Skills Únicas", "ov-kpi-skills", "#10b981"), md=3),
        dbc.Col(kpi_card("bi-currency-dollar", "Salário Médio", "ov-kpi-salary", "#f59e0b"), md=3),
    ], className="mb-4 g-3"),

    # Row 1: Senioridade + Modalidade
    dbc.Row([
        dbc.Col(chart_card("ov-chart-seniority"), md=6),
        dbc.Col(chart_card("ov-chart-modality"), md=6),
    ], className="mb-4 g-3"),

    # Row 2: Indústria
    dbc.Row(
        dbc.Col(chart_card("ov-chart-industry")),
        className="mb-4",
    ),
])


@callback(
    [
        dash.Output("ov-kpi-jobs", "children"),
        dash.Output("ov-kpi-companies", "children"),
        dash.Output("ov-kpi-skills", "children"),
        dash.Output("ov-kpi-salary", "children"),
        dash.Output("ov-chart-seniority", "figure"),
        dash.Output("ov-chart-modality", "figure"),
        dash.Output("ov-chart-industry", "figure"),
    ],
    [
        dash.Input("ov-filter-seniority", "value"),
        dash.Input("ov-filter-status", "value"),
        dash.Input("ov-filter-industry", "value"),
    ],
)
def update_overview(seniority, status, industry):
    dff, dff_skills = prep.apply_filters(df, skills_df, seniority, status, industry)
    kpis = prep.get_overview_kpis(dff, dff_skills)

    salary_str = f"${kpis['salary_avg']:,.0f}" if kpis["salary_avg"] else "N/A"

    return (
        f"{kpis['total_jobs']:,}",
        f"{kpis['total_companies']:,}",
        f"{kpis['total_skills']:,}",
        salary_str,
        charts.make_seniority_distribution_chart(dff),
        charts.make_jobs_by_modality_chart(dff),
        charts.make_industry_distribution_chart(dff),
    )
