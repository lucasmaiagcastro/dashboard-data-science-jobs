import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

import src.preprocessing as prep
import src.charts as charts

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
    title="Data Science Jobs 2025",
)
server = app.server

df, skills_df = prep.load_data()

SENIORITY_OPTIONS = [
    {"label": "Junior", "value": "junior"},
    {"label": "Mid-level", "value": "midlevel"},
    {"label": "Senior", "value": "senior"},
    {"label": "Lead", "value": "lead"},
    {"label": "N/A", "value": "Não informado"},
]

STATUS_OPTIONS = [
    {"label": "Presencial", "value": "on-site"},
    {"label": "Híbrido", "value": "hybrid"},
    {"label": "Remoto", "value": "remote"},
    {"label": "N/A", "value": "Não informado"},
]

INDUSTRY_OPTIONS = [
    {"label": i, "value": i}
    for i in sorted(df["industry"].unique())
    if i != "Não informado"
]

DROPDOWN_STYLE = {
    "borderRadius": "8px",
    "fontSize": "13px",
}


def kpi_card(icon, label, value_id, color):
    return dbc.Card(
        dbc.CardBody(
            html.Div(
                [
                    html.Div(
                        html.I(className=f"bi {icon}", style={"fontSize": "1.8rem", "color": color}),
                        className="d-flex align-items-center justify-content-center rounded-3 p-2",
                        style={"background": f"{color}22", "width": "52px", "height": "52px"},
                    ),
                    html.Div(
                        [
                            html.P(label, className="text-muted mb-0", style={"fontSize": "12px"}),
                            html.H5(id=value_id, className="fw-bold mb-0", style={"color": color}),
                        ],
                        className="ms-3",
                    ),
                ],
                className="d-flex align-items-center",
            )
        ),
        className="border-0 shadow-sm h-100",
        style={"background": "#1e293b", "borderRadius": "12px"},
    )


def chart_card(graph_id):
    return dbc.Card(
        dbc.CardBody(
            dcc.Graph(id=graph_id, config={"displayModeBar": False}, style={"borderRadius": "8px"})
        ),
        className="border-0 shadow-sm h-100",
        style={"background": "#1e293b", "borderRadius": "12px"},
    )


app.layout = dbc.Container(
    [
        # ── Header ──────────────────────────────────────────────────────────
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span("DS", style={
                                    "background": "linear-gradient(135deg,#6366f1,#06b6d4)",
                                    "WebkitBackgroundClip": "text",
                                    "WebkitTextFillColor": "transparent",
                                    "fontWeight": "800",
                                    "fontSize": "2rem",
                                }),
                                html.Span(" Jobs", style={"fontWeight": "300", "fontSize": "2rem"}),
                            ]
                        ),
                        html.P(
                            "Análise do mercado de Ciência de Dados · 944 vagas · 2025",
                            className="text-muted mb-0",
                            style={"fontSize": "13px"},
                        ),
                    ],
                    className="py-4",
                )
            )
        ),

        # ── Filters ─────────────────────────────────────────────────────────
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Senioridade", className="text-muted", style={"fontSize": "12px"}),
                        dcc.Dropdown(
                            id="filter-seniority",
                            options=SENIORITY_OPTIONS,
                            multi=True,
                            placeholder="Todos os níveis...",
                            style=DROPDOWN_STYLE,
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        dbc.Label("Modalidade", className="text-muted", style={"fontSize": "12px"}),
                        dcc.Dropdown(
                            id="filter-status",
                            options=STATUS_OPTIONS,
                            multi=True,
                            placeholder="Todas as modalidades...",
                            style=DROPDOWN_STYLE,
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        dbc.Label("Indústria", className="text-muted", style={"fontSize": "12px"}),
                        dcc.Dropdown(
                            id="filter-industry",
                            options=INDUSTRY_OPTIONS,
                            multi=True,
                            placeholder="Todas as indústrias...",
                            style=DROPDOWN_STYLE,
                        ),
                    ],
                    md=4,
                ),
            ],
            className="mb-4 g-3",
        ),

        # ── KPI Cards ───────────────────────────────────────────────────────
        dbc.Row(
            [
                dbc.Col(kpi_card("bi-briefcase-fill", "Total de Vagas", "kpi-total", "#6366f1"), md=3),
                dbc.Col(kpi_card("bi-currency-dollar", "Salário Médio", "kpi-salary", "#06b6d4"), md=3),
                dbc.Col(kpi_card("bi-laptop-fill", "Trabalho Remoto", "kpi-remote", "#10b981"), md=3),
                dbc.Col(kpi_card("bi-star-fill", "Skill Mais Pedida", "kpi-skill", "#f59e0b"), md=3),
            ],
            className="mb-4 g-3",
        ),

        # ── Row 1: Skills + Modality ─────────────────────────────────────────
        dbc.Row(
            [
                dbc.Col(chart_card("chart-skills"), md=8),
                dbc.Col(chart_card("chart-modality"), md=4),
            ],
            className="mb-4 g-3",
        ),

        # ── Row 2: Salary Industry + Salary Seniority ────────────────────────
        dbc.Row(
            [
                dbc.Col(chart_card("chart-salary-industry"), md=6),
                dbc.Col(chart_card("chart-salary-seniority"), md=6),
            ],
            className="mb-4 g-3",
        ),

        # ── Row 3: Salary by Skill ───────────────────────────────────────────
        dbc.Row(
            dbc.Col(chart_card("chart-salary-skill")),
            className="mb-4",
        ),

        # ── Footer ───────────────────────────────────────────────────────────
        dbc.Row(
            dbc.Col(
                html.P(
                    "Dashboard de Vagas em Ciência de Dados · Visualização de Dados · Unichristus 2026",
                    className="text-muted text-center py-3 mb-0",
                    style={"fontSize": "12px", "borderTop": "1px solid #1e293b"},
                )
            )
        ),
    ],
    fluid=True,
    style={"backgroundColor": "#0f172a", "minHeight": "100vh", "padding": "0 2rem"},
)


@app.callback(
    [
        Output("kpi-total", "children"),
        Output("kpi-salary", "children"),
        Output("kpi-remote", "children"),
        Output("kpi-skill", "children"),
        Output("chart-skills", "figure"),
        Output("chart-modality", "figure"),
        Output("chart-salary-industry", "figure"),
        Output("chart-salary-seniority", "figure"),
        Output("chart-salary-skill", "figure"),
    ],
    [
        Input("filter-seniority", "value"),
        Input("filter-status", "value"),
        Input("filter-industry", "value"),
    ],
)
def update_dashboard(seniority, status, industry):
    dff, dff_skills = prep.apply_filters(df, skills_df, seniority, status, industry)
    kpis = prep.get_kpis(dff, dff_skills)

    salary_str = f"${kpis['salary_avg']:,.0f}" if kpis["salary_avg"] else "N/A"

    return (
        f"{kpis['total']:,}",
        salary_str,
        f"{kpis['remote_pct']:.1f}%",
        kpis["top_skill"].title(),
        charts.make_top_skills_chart(dff_skills),
        charts.make_jobs_by_modality_chart(dff),
        charts.make_salary_by_industry_chart(dff),
        charts.make_salary_by_seniority_chart(dff),
        charts.make_salary_by_skill_chart(dff_skills),
    )


if __name__ == "__main__":
    app.run(debug=True)
