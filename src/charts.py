import plotly.graph_objects as go
import src.preprocessing as prep

PALETTE = ["#6366f1", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#f97316"]
PRIMARY = "#6366f1"
FONT_COLOR = "#e2e8f0"
TRANSPARENT = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(255,255,255,0.07)"
FONT_FAMILY = "Inter, system-ui, sans-serif"
HEATMAP_SCALE = [[0, "#0f172a"], [0.4, "#4338ca"], [1, "#06b6d4"]]


def _base(height=400, margin=None):
    default_margin = dict(l=48, r=48, t=52, b=48)
    if margin:
        default_margin.update(margin)
    return dict(
        paper_bgcolor=TRANSPARENT,
        plot_bgcolor=TRANSPARENT,
        font=dict(color=FONT_COLOR, family=FONT_FAMILY, size=13),
        margin=default_margin,
        height=height,
    )


def _yaxis_labels():
    return dict(showgrid=False, automargin=True, ticklabelstandoff=14)


def _xaxis_labels(**kwargs):
    return dict(showgrid=False, automargin=True, ticklabelstandoff=10, **kwargs)


def _empty(title, height=400):
    fig = go.Figure()
    fig.update_layout(
        **_base(height),
        title=dict(text=title, font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[dict(text="Sem dados para os filtros selecionados", showarrow=False,
                          font=dict(color="#64748b", size=14))],
    )
    return fig


# ── Overview ─────────────────────────────────────────────────────────────────

def make_seniority_distribution_chart(df):
    counts = prep.get_jobs_by_seniority(df)
    if counts.empty:
        return _empty("Vagas por Senioridade", 360)

    fig = go.Figure(go.Bar(
        x=counts["count"],
        y=counts["label"],
        orientation="h",
        marker=dict(color=PALETTE[: len(counts)]),
        text=counts["count"],
        textposition="outside",
        textfont=dict(color=FONT_COLOR),
        hovertemplate="<b>%{y}</b>: %{x} vagas<extra></extra>",
    ))
    fig.update_layout(
        **_base(360, margin=dict(l=100, r=56)),
        title=dict(text="Vagas por Senioridade", font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=_yaxis_labels(),
    )
    return fig


def make_industry_distribution_chart(df):
    counts = prep.get_jobs_by_industry(df)
    if counts.empty:
        return _empty("Vagas por Indústria", 360)

    fig = go.Figure(go.Bar(
        x=counts["count"],
        y=counts["label"],
        orientation="h",
        marker=dict(
            color=counts["count"],
            colorscale=[[0, "#312e81"], [1, "#06b6d4"]],
            showscale=False,
        ),
        text=counts["count"],
        textposition="outside",
        textfont=dict(color=FONT_COLOR),
        hovertemplate="<b>%{y}</b>: %{x} vagas<extra></extra>",
    ))
    fig.update_layout(
        **_base(360, margin=dict(l=120, r=56)),
        title=dict(text="Vagas por Indústria", font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=_yaxis_labels(),
    )
    return fig


def make_jobs_by_modality_chart(df):
    counts = prep.get_jobs_by_modality(df)
    if counts.empty:
        return _empty("Modalidade de Trabalho", 360)

    fig = go.Figure(go.Pie(
        labels=counts["label"],
        values=counts["count"],
        hole=0.58,
        marker=dict(colors=PALETTE, line=dict(color="#0f172a", width=2)),
        textinfo="label+percent",
        textfont=dict(color=FONT_COLOR, size=12),
        hovertemplate="<b>%{label}</b><br>%{value} vagas (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        **_base(360),
        title=dict(text="Modalidade de Trabalho", font=dict(size=15, color=FONT_COLOR)),
        showlegend=False,
    )
    return fig


# ── Skills ───────────────────────────────────────────────────────────────────

def make_top_skills_chart(skills_df, n=15):
    counts = prep.get_top_skills(skills_df, n)
    if counts.empty:
        return _empty("Skills Mais Demandadas", 460)

    fig = go.Figure(go.Bar(
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
    ))
    fig.update_layout(
        **_base(460, margin=dict(l=130, r=56)),
        title=dict(text="Skills Mais Demandadas", font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis={**_yaxis_labels(), "tickfont": dict(size=12)},
    )
    return fig


def make_skills_heatmap_by_seniority(skills_df):
    pivot = prep.get_skills_by_seniority(skills_df)
    if pivot.empty:
        return _empty("Skills por Senioridade", 460)

    norm = pivot.div(pivot.sum(axis=0), axis=1).mul(100).round(1)

    fig = go.Figure(go.Heatmap(
        z=norm.values,
        x=norm.columns.tolist(),
        y=norm.index.tolist(),
        colorscale=HEATMAP_SCALE,
        showscale=True,
        hovertemplate="<b>%{y}</b> · <b>%{x}</b><br>%{z:.1f}% das menções<extra></extra>",
        colorbar=dict(ticksuffix="%", tickfont=dict(color=FONT_COLOR), outlinewidth=0),
    ))
    fig.update_layout(
        **_base(460, margin=dict(l=130, r=72, b=56)),
        title=dict(text="Skills por Senioridade (% das menções)", font=dict(size=15, color=FONT_COLOR)),
        xaxis=_xaxis_labels(),
        yaxis={**_yaxis_labels(), "tickfont": dict(size=12)},
    )
    return fig


def make_skills_heatmap_by_industry(skills_df):
    pivot = prep.get_skills_by_industry(skills_df)
    if pivot.empty:
        return _empty("Skills por Indústria", 440)

    norm = pivot.div(pivot.sum(axis=0), axis=1).mul(100).round(1)

    fig = go.Figure(go.Heatmap(
        z=norm.values,
        x=norm.columns.tolist(),
        y=norm.index.tolist(),
        colorscale=HEATMAP_SCALE,
        showscale=True,
        hovertemplate="<b>%{y}</b> · <b>%{x}</b><br>%{z:.1f}%<extra></extra>",
        colorbar=dict(ticksuffix="%", tickfont=dict(color=FONT_COLOR), outlinewidth=0),
    ))
    fig.update_layout(
        **_base(440, margin=dict(l=130, r=72, b=72)),
        title=dict(text="Skills por Indústria (% das menções)", font=dict(size=15, color=FONT_COLOR)),
        xaxis=_xaxis_labels(tickangle=-25),
        yaxis={**_yaxis_labels(), "tickfont": dict(size=12)},
    )
    return fig


# ── Salaries ─────────────────────────────────────────────────────────────────

def make_salary_histogram(df):
    data = df["salary_avg_adjusted"].dropna() / 1000
    if data.empty:
        return _empty("Distribuição de Salários", 400)

    fig = go.Figure(go.Histogram(
        x=data,
        nbinsx=30,
        marker=dict(color=PRIMARY, opacity=0.85, line=dict(color="#0f172a", width=0.5)),
        hovertemplate="$%{x:.0f}k — %{y} vagas<extra></extra>",
    ))
    fig.update_layout(
        **_base(400),
        title=dict(text="Distribuição de Salários (US$k)", font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(showgrid=False, tickprefix="$", ticksuffix="k"),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR),
        bargap=0.05,
    )
    return fig


def make_salary_boxplot_by_seniority(df):
    order = ["junior", "midlevel", "senior", "lead"]
    fig = go.Figure()
    for i, sen in enumerate(order):
        subset = df[df["seniority_level"] == sen]["salary_avg_adjusted"] / 1000
        if not subset.empty:
            label = prep.SENIORITY_LABELS.get(sen, sen)
            fig.add_trace(go.Box(
                y=subset,
                name=label,
                marker_color=PALETTE[i % len(PALETTE)],
                line=dict(width=1.5),
                boxmean="sd",
                hovertemplate=f"<b>{label}</b><br>Mediana: $%{{median:.0f}}k<extra></extra>",
            ))
    if not fig.data:
        return _empty("Distribuição Salarial por Senioridade", 420)

    fig.update_layout(
        **_base(420, margin=dict(b=56)),
        title=dict(text="Distribuição Salarial por Senioridade (US$k)", font=dict(size=15, color=FONT_COLOR)),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, tickprefix="$", ticksuffix="k", zeroline=False),
        xaxis=_xaxis_labels(),
        showlegend=False,
    )
    return fig


def make_salary_by_industry_chart(df):
    dff, order = prep.get_salary_by_industry(df)
    if not order:
        return _empty("Distribuição Salarial por Indústria", 420)

    fig = go.Figure()
    for i, industry in enumerate(order):
        label = prep.INDUSTRY_LABELS.get(industry, industry)
        subset = dff[dff["industry"] == industry]["salary_avg_adjusted"] / 1000
        fig.add_trace(go.Box(
            y=subset,
            name=label,
            marker_color=PALETTE[i % len(PALETTE)],
            line=dict(width=1.5),
            boxmean="sd",
            hovertemplate=f"<b>{label}</b><br>Mediana: $%{{median:.0f}}k<extra></extra>",
        ))
    fig.update_layout(
        **_base(420, margin=dict(b=72)),
        title=dict(text="Distribuição Salarial por Indústria (US$k)", font=dict(size=15, color=FONT_COLOR)),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, tickprefix="$", ticksuffix="k", zeroline=False),
        xaxis=_xaxis_labels(tickangle=-25),
        showlegend=False,
    )
    return fig


def make_salary_by_seniority_chart(df):
    dff = prep.get_salary_by_seniority(df)
    if dff.empty:
        return _empty("Salário por Senioridade", 400)

    fig = go.Figure(go.Bar(
        x=dff["label"],
        y=dff["salary_k"],
        marker=dict(color=PALETTE[: len(dff)]),
        text=dff["salary_k"].map("${:.0f}k".format),
        textposition="outside",
        textfont=dict(color=FONT_COLOR, size=13),
        hovertemplate="<b>%{x}</b><br>Mediana: $%{y:.0f}k<extra></extra>",
    ))
    fig.update_layout(
        **_base(400, margin=dict(b=56)),
        title=dict(text="Salário Mediano por Senioridade (US$k)", font=dict(size=15, color=FONT_COLOR)),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, tickprefix="$", ticksuffix="k", zeroline=False),
        xaxis=_xaxis_labels(),
    )
    return fig


def make_salary_by_skill_chart(skills_df, n=12):
    dff = prep.get_salary_by_skill(skills_df, n)
    if dff.empty:
        return _empty("Salário por Skill", 400)

    fig = go.Figure(go.Bar(
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
    ))
    fig.update_layout(
        **_base(400, margin=dict(b=88)),
        title=dict(text="Salário Mediano por Skill — Top 12 (US$k)", font=dict(size=15, color=FONT_COLOR)),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, tickprefix="$", ticksuffix="k", zeroline=False),
        xaxis=_xaxis_labels(tickangle=-30),
    )
    return fig


# ── Market ───────────────────────────────────────────────────────────────────

def make_ownership_chart(df):
    counts = prep.get_ownership_distribution(df)
    if counts.empty:
        return _empty("Tipo de Empresa", 420)

    fig = go.Figure(go.Pie(
        labels=counts["ownership"],
        values=counts["count"],
        hole=0.58,
        marker=dict(colors=[PALETTE[0], PALETTE[1]], line=dict(color="#0f172a", width=2)),
        textinfo="label+percent",
        textfont=dict(color=FONT_COLOR, size=13),
        hovertemplate="<b>%{label}</b><br>%{value} vagas (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        **_base(420),
        title=dict(text="Tipo de Empresa (Capital Aberto vs Fechado)", font=dict(size=15, color=FONT_COLOR)),
        showlegend=False,
    )
    return fig


def make_avg_skills_by_seniority_chart(df):
    dff = prep.get_avg_skills_by_seniority(df)
    if dff.empty:
        return _empty("Skills Exigidas por Senioridade", 420)

    fig = go.Figure(go.Bar(
        x=dff["label"],
        y=dff["avg_skills"],
        marker=dict(color=PALETTE[: len(dff)]),
        text=dff["avg_skills"].map("{:.1f}".format),
        textposition="outside",
        textfont=dict(color=FONT_COLOR, size=13),
        hovertemplate="<b>%{x}</b><br>Média: %{y:.1f} skills por vaga<extra></extra>",
    ))
    fig.update_layout(
        **_base(420, margin=dict(b=56)),
        title=dict(text="Média de Skills Exigidas por Senioridade", font=dict(size=15, color=FONT_COLOR)),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False, title="Média de skills"),
        xaxis=_xaxis_labels(),
    )
    return fig


def make_company_size_chart(df):
    counts = prep.get_jobs_by_company_size(df)
    if counts.empty:
        return _empty("Vagas por Tamanho de Empresa", 380)

    fig = go.Figure(go.Bar(
        x=counts["size_cat"],
        y=counts["count"],
        marker=dict(color=PALETTE[: len(counts)]),
        text=counts["count"],
        textposition="outside",
        textfont=dict(color=FONT_COLOR),
        hovertemplate="<b>%{x}</b>: %{y} vagas<extra></extra>",
    ))
    fig.update_layout(
        **_base(380, margin=dict(b=72)),
        title=dict(text="Vagas por Tamanho de Empresa", font=dict(size=15, color=FONT_COLOR)),
        xaxis=_xaxis_labels(tickangle=-20),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False),
    )
    return fig
