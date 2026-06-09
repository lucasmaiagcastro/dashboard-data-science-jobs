import pandas as pd

JOBS_PATH = "data/data_science_jobs_clean.csv"
SKILLS_PATH = "data/data_science_jobs_skills_clean.csv"

SENIORITY_LABELS = {
    "junior": "Junior",
    "midlevel": "Mid-level",
    "senior": "Senior",
    "lead": "Lead",
    "Não informado": "N/A",
}

STATUS_LABELS = {
    "on-site": "Presencial",
    "hybrid": "Híbrido",
    "remote": "Remoto",
    "Não informado": "N/A",
}


def load_data():
    df = pd.read_csv(JOBS_PATH)
    skills_df = pd.read_csv(SKILLS_PATH)
    df = df.dropna(subset=["salary_avg_adjusted"])
    skills_df = skills_df.dropna(subset=["salary_avg_adjusted"])
    return df, skills_df


def apply_filters(df, skills_df, seniority=None, status=None, industry=None):
    dff = df.copy()
    dff_skills = skills_df.copy()
    if seniority:
        dff = dff[dff["seniority_level"].isin(seniority)]
        dff_skills = dff_skills[dff_skills["seniority_level"].isin(seniority)]
    if status:
        dff = dff[dff["status"].isin(status)]
        dff_skills = dff_skills[dff_skills["status"].isin(status)]
    if industry:
        dff = dff[dff["industry"].isin(industry)]
        dff_skills = dff_skills[dff_skills["industry"].isin(industry)]
    return dff, dff_skills


# ── KPIs ────────────────────────────────────────────────────────────────────

def get_kpis(df, skills_df):
    total = len(df)
    return {
        "total": total,
        "salary_avg": df["salary_avg_adjusted"].mean() if total > 0 else None,
        "remote_pct": (df["is_remote"].sum() / total * 100) if total > 0 else 0,
        "top_skill": skills_df["skill"].value_counts().index[0] if len(skills_df) > 0 else "N/A",
    }


def get_overview_kpis(df, skills_df):
    total = len(df)
    return {
        "total_jobs": total,
        "total_companies": df["company"].nunique(),
        "total_skills": skills_df["skill"].nunique() if len(skills_df) > 0 else 0,
        "salary_avg": df["salary_avg_adjusted"].mean() if total > 0 else None,
    }


# ── Overview ─────────────────────────────────────────────────────────────────

def get_jobs_by_seniority(df):
    order = ["junior", "midlevel", "senior", "lead", "Não informado"]
    counts = (
        df["seniority_level"].value_counts()
        .reindex(order)
        .dropna()
        .reset_index()
    )
    counts.columns = ["seniority_level", "count"]
    counts["label"] = counts["seniority_level"].map(SENIORITY_LABELS).fillna(counts["seniority_level"])
    return counts


def get_jobs_by_industry(df):
    counts = df["industry"].value_counts().reset_index()
    counts.columns = ["industry", "count"]
    return counts.sort_values("count")


def get_jobs_by_modality(df):
    counts = df["status"].value_counts().reset_index()
    counts.columns = ["status", "count"]
    counts["label"] = counts["status"].map(STATUS_LABELS).fillna(counts["status"])
    return counts


# ── Skills ───────────────────────────────────────────────────────────────────

def get_top_skills(skills_df, n=15):
    counts = skills_df["skill"].value_counts().head(n).reset_index()
    counts.columns = ["skill", "count"]
    return counts.sort_values("count")


def get_skills_by_seniority(skills_df, n_skills=10):
    order = ["junior", "midlevel", "senior", "lead"]
    top_skills = skills_df["skill"].value_counts().head(n_skills).index
    dff = skills_df[
        skills_df["skill"].isin(top_skills) & skills_df["seniority_level"].isin(order)
    ]
    pivot = dff.groupby(["skill", "seniority_level"]).size().unstack(fill_value=0)
    pivot = pivot.reindex(columns=[c for c in order if c in pivot.columns])
    pivot.columns = [SENIORITY_LABELS.get(c, c) for c in pivot.columns]
    return pivot


def get_skills_by_industry(skills_df, n_skills=8):
    valid = [i for i in skills_df["industry"].unique() if i != "Não informado"]
    top_skills = skills_df["skill"].value_counts().head(n_skills).index
    dff = skills_df[skills_df["skill"].isin(top_skills) & skills_df["industry"].isin(valid)]
    pivot = dff.groupby(["skill", "industry"]).size().unstack(fill_value=0)
    return pivot


# ── Salaries ─────────────────────────────────────────────────────────────────

def get_salary_by_industry(df):
    valid = df[~df["industry"].isin(["Não informado"])]
    order = (
        valid.groupby("industry")["salary_avg_adjusted"]
        .median()
        .sort_values(ascending=False)
        .index.tolist()
    )
    return valid, order


def get_salary_by_seniority(df):
    order = ["junior", "midlevel", "senior", "lead"]
    dff = (
        df[df["seniority_level"].isin(order)]
        .groupby("seniority_level")["salary_avg_adjusted"]
        .median()
        .reindex(order)
        .dropna()
        .reset_index()
    )
    dff["label"] = dff["seniority_level"].map(SENIORITY_LABELS)
    dff["salary_k"] = dff["salary_avg_adjusted"] / 1000
    return dff


def get_salary_by_skill(skills_df, n=12):
    top_skills = skills_df["skill"].value_counts().head(n).index
    dff = (
        skills_df[skills_df["skill"].isin(top_skills)]
        .groupby("skill")["salary_avg_adjusted"]
        .median()
        .sort_values(ascending=False)
        .reset_index()
    )
    dff["salary_k"] = dff["salary_avg_adjusted"] / 1000
    return dff


# ── Market ───────────────────────────────────────────────────────────────────

def get_top_companies(df, n=12):
    counts = df["company"].value_counts().head(n).reset_index()
    counts.columns = ["company", "count"]
    counts["label"] = counts["company"].str.replace(r"company_0*(\d+)", r"Empresa \1", regex=True)
    return counts.sort_values("count")


def get_top_locations(df, n=12):
    def extract_state(hq):
        parts = str(hq).split(", ")
        return parts[1] if len(parts) >= 3 else parts[0]

    dff = df.copy()
    dff["state"] = dff["headquarter"].apply(extract_state)
    counts = dff["state"].value_counts().head(n).reset_index()
    counts.columns = ["state", "count"]
    return counts.sort_values("count")


def get_jobs_by_company_size(df):
    SIZE_ORDER = ["Pequena (<1k)", "Média (1k–10k)", "Grande (10k–100k)", "Muito Grande (>100k)"]

    def categorize(val):
        try:
            n = int(str(val).replace(",", "").replace(".", "").split()[0])
            if n < 1_000:
                return "Pequena (<1k)"
            elif n < 10_000:
                return "Média (1k–10k)"
            elif n < 100_000:
                return "Grande (10k–100k)"
            else:
                return "Muito Grande (>100k)"
        except (ValueError, TypeError):
            return None

    dff = df.copy()
    dff["size_cat"] = dff["company_size"].apply(categorize)
    counts = (
        dff["size_cat"].value_counts()
        .reindex(SIZE_ORDER)
        .dropna()
        .reset_index()
    )
    counts.columns = ["size_cat", "count"]
    return counts
