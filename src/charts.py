import plotly.graph_objects as go
import src.preprocessing as prep

PALETTE = ["#6366f1", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#f97316"]
FONT_COLOR = "#e2e8f0"
TRANSPARENT = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(255,255,255,0.07)"
FONT_FAMILY = "Inter, system-ui, sans-serif"


def _base(height=400):
    return dict(
        paper_bgcolor=TRANSPARENT,
        plot_bgcolor=TRANSPARENT,
        font=dict(color=FONT_COLOR, family=FONT_FAMILY, size=13),
        margin=dict(l=10, r=20, t=48, b=10),
        height=height,
    )


def make_top_skills_chart(skills_df, n=15):
    counts = prep.get_top_skills(skills_df, n)

    fig = go.Figure(
        go.Bar(
            x=counts["count"],
            y=counts["skill"],
            orientation="h",
            marker=dict(
                color=counts["count"],
                colorscale=[[0, "#3730a3"], [0.5, "#6366f1"], [1, "#06b6d4"]],
                showscale=False,
            ),
            text=counts["count"],
            textposition="outside",
            textfont=dict(color=FONT_COLOR, size=12),
            hovertemplate="<b>%{y}</b><br>Vagas: %{x}<extra></extra>",
        )
    )
    fig.update_layout(
        **_base(440),
        title=dict(text="Skills Mais Demandadas", font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=12)),
    )
    return fig


def make_jobs_by_modality_chart(df):
    counts = prep.get_jobs_by_modality(df)

    fig = go.Figure(
        go.Pie(
            labels=counts["label"],
            values=counts["count"],
            hole=0.58,
            marker=dict(colors=PALETTE, line=dict(color="#0f172a", width=2)),
            textinfo="label+percent",
            textfont=dict(color=FONT_COLOR, size=12),
            hovertemplate="<b>%{label}</b><br>%{value} vagas (%{percent})<extra></extra>",
        )
    )
    fig.update_layout(
        **_base(440),
        title=dict(text="Modalidade de Trabalho", font=dict(size=15, color=FONT_COLOR)),
        showlegend=False,
    )
    return fig


def make_salary_by_industry_chart(df):
    dff, order = prep.get_salary_by_industry(df)

    fig = go.Figure()
    for i, industry in enumerate(order):
        subset = dff[dff["industry"] == industry]["salary_avg_adjusted"] / 1000
        fig.add_trace(
            go.Box(
                y=subset,
                name=industry,
                marker_color=PALETTE[i % len(PALETTE)],
                line=dict(width=1.5),
                boxmean="sd",
                hovertemplate=f"<b>{industry}</b><br>Mediana: $%{{median:.0f}}k<extra></extra>",
            )
        )
    fig.update_layout(
        **_base(420),
        title=dict(text="Distribuição Salarial por Indústria (US$k)", font=dict(size=15, color=FONT_COLOR)),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID_COLOR,
            tickprefix="$",
            ticksuffix="k",
            zeroline=False,
        ),
        xaxis=dict(showgrid=False),
        showlegend=False,
    )
    return fig


def make_salary_by_seniority_chart(df):
    dff = prep.get_salary_by_seniority(df)

    if dff.empty:
        return go.Figure().update_layout(**_base(400), title="Salário por Senioridade")

    fig = go.Figure(
        go.Bar(
            x=dff["label"],
            y=dff["salary_k"],
            marker=dict(color=PALETTE[: len(dff)]),
            text=dff["salary_k"].map("${:.0f}k".format),
            textposition="outside",
            textfont=dict(color=FONT_COLOR, size=13),
            hovertemplate="<b>%{x}</b><br>Mediana: $%{y:.0f}k<extra></extra>",
        )
    )
    fig.update_layout(
        **_base(400),
        title=dict(text="Salário Mediano por Senioridade (US$k)", font=dict(size=15, color=FONT_COLOR)),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID_COLOR,
            tickprefix="$",
            ticksuffix="k",
            zeroline=False,
        ),
        xaxis=dict(showgrid=False),
    )
    return fig


def make_salary_by_skill_chart(skills_df, n=12):
    dff = prep.get_salary_by_skill(skills_df, n)

    if dff.empty:
        return go.Figure().update_layout(**_base(380), title="Salário por Skill")

    fig = go.Figure(
        go.Bar(
            x=dff["skill"],
            y=dff["salary_k"],
            marker=dict(
                color=dff["salary_k"],
                colorscale=[[0, "#3730a3"], [0.5, "#6366f1"], [1, "#06b6d4"]],
                showscale=False,
            ),
            text=dff["salary_k"].map("${:.0f}k".format),
            textposition="outside",
            textfont=dict(color=FONT_COLOR, size=12),
            hovertemplate="<b>%{x}</b><br>Mediana: $%{y:.0f}k<extra></extra>",
        )
    )
    fig.update_layout(
        **_base(400),
        title=dict(text="Salário Mediano por Skill — Top 12 (US$k)", font=dict(size=15, color=FONT_COLOR)),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID_COLOR,
            tickprefix="$",
            ticksuffix="k",
            zeroline=False,
        ),
        xaxis=dict(showgrid=False, tickangle=-30),
    )
    return fig
