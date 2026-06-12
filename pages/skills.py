import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc

import src.charts as charts
import src.preprocessing as prep
from src.data import df, skills_df

dash.register_page(__name__, path="/skills", name="Skills")

SENIORITY_OPTIONS = [
    {"label": "Junior", "value": "junior"},
    {"label": "Mid-level", "value": "midlevel"},
    {"label": "Senior", "value": "senior"},
    {"label": "Lead", "value": "lead"},
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
        html.H2("Skills e Tecnologias", className="fw-bold mb-1"),
        html.P("Quais habilidades o mercado mais exige e como elas se distribuem", className="text-muted mb-0", style={"fontSize": "14px"}),
    ], className="mb-4"),

    # Filters
    dbc.Card(
        dbc.CardBody(
            dbc.Row([
                dbc.Col([
                    dbc.Label("Senioridade", className="text-muted", style={"fontSize": "12px"}),
                    dcc.Dropdown(id="sk-filter-seniority", options=SENIORITY_OPTIONS, multi=True, placeholder="Todos os níveis..."),
                ], md=6),
                dbc.Col([
                    dbc.Label("Indústria", className="text-muted", style={"fontSize": "12px"}),
                    dcc.Dropdown(id="sk-filter-industry", options=INDUSTRY_OPTIONS, multi=True, placeholder="Todas as indústrias..."),
                ], md=6),
            ], className="g-3")
        ),
        className="border-0 mb-4 filter-card",
        style=CARD_STYLE,
    ),

    # Row 1: Top skills + Heatmap senioridade
    dbc.Row([
        dbc.Col(chart_card("sk-chart-top-skills"), md=7),
        dbc.Col(chart_card("sk-chart-heatmap-seniority"), md=5),
    ], className="mb-4 g-3"),

    # Row 2: Heatmap indústria
    dbc.Row(
        dbc.Col(chart_card("sk-chart-heatmap-industry")),
        className="mb-4",
    ),
])


@callback(
    [
        dash.Output("sk-chart-top-skills", "figure"),
        dash.Output("sk-chart-heatmap-seniority", "figure"),
        dash.Output("sk-chart-heatmap-industry", "figure"),
    ],
    [
        dash.Input("sk-filter-seniority", "value"),
        dash.Input("sk-filter-industry", "value"),
    ],
)
def update_skills(seniority, industry):
    dff, dff_skills = prep.apply_filters(df, skills_df, seniority=seniority, industry=industry)
    return (
        charts.make_top_skills_chart(dff_skills),
        charts.make_skills_heatmap_by_seniority(dff_skills),
        charts.make_skills_heatmap_by_industry(dff_skills),
    )
