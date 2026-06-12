"""Carrega os datasets uma vez na inicialização do app."""
from src.preprocessing import load_data

df, skills_df = load_data()
