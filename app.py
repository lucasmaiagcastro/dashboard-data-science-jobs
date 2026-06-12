"""Entry point do dashboard Dash (multi-page).

Configura navbar, layout global e expõe `server` pro deploy na Plotly Cloud.
"""
import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
    title="DS Jobs 2025",
)
server = app.server

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(
                [
                    html.Span("DS", className="brand-ds"),
                    html.Span(" Jobs", style={"fontWeight": "300"}),
                    html.Span(" 2025", style={"fontWeight": "300", "color": "#64748b", "fontSize": "0.9rem"}),
                ],
                href="/",
                className="me-4",
                style={"fontSize": "1.35rem", "letterSpacing": "-0.5px"},
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink(
                            [html.I(className="bi bi-grid-fill me-1"), "Visão Geral"],
                            href="/", active="exact",
                        )),
                        dbc.NavItem(dbc.NavLink(
                            [html.I(className="bi bi-lightning-fill me-1"), "Skills"],
                            href="/skills", active="exact",
                        )),
                        dbc.NavItem(dbc.NavLink(
                            [html.I(className="bi bi-currency-dollar me-1"), "Salários"],
                            href="/salarios", active="exact",
                        )),
                        dbc.NavItem(dbc.NavLink(
                            [html.I(className="bi bi-buildings-fill me-1"), "Mercado"],
                            href="/mercado", active="exact",
                        )),
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="#1e293b",
    dark=True,
    sticky="top",
    style={"borderBottom": "1px solid #334155"},
)

app.layout = html.Div(
    [
        navbar,
        dbc.Container(
            dash.page_container,
            fluid=True,
            style={"minHeight": "calc(100vh - 60px)", "padding": "2rem 2.5rem 1rem"},
        ),
        html.Footer(
            "Dashboard de Vagas em Ciência de Dados · Visualização de Dados · Unichristus 2026",
            style={
                "textAlign": "center",
                "color": "#475569",
                "fontSize": "12px",
                "padding": "1rem",
                "borderTop": "1px solid #1e293b",
            },
        ),
    ],
    style={"backgroundColor": "#0f172a"},
)

if __name__ == "__main__":
    app.run(debug=True)
