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


def get_kpis(df, skills_df):
    total = len(df)
    salary_avg = df["salary_avg_adjusted"].mean() if total > 0 else None
    remote_pct = (df["is_remote"].sum() / total * 100) if total > 0 else 0
    top_skill = skills_df["skill"].value_counts().index[0] if len(skills_df) > 0 else "N/A"
    return {
        "total": total,
        "salary_avg": salary_avg,
        "remote_pct": remote_pct,
        "top_skill": top_skill,
    }


def get_top_skills(skills_df, n=15):
    counts = skills_df["skill"].value_counts().head(n).reset_index()
    counts.columns = ["skill", "count"]
    return counts.sort_values("count")


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


def get_jobs_by_modality(df):
    counts = df["status"].value_counts().reset_index()
    counts.columns = ["status", "count"]
    counts["label"] = counts["status"].map(STATUS_LABELS).fillna(counts["status"])
    return counts
