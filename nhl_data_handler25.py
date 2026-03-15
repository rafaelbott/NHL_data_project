import pandas as pd
import os
from nhl_scraper10 import load_nhl_data

path = r"donnes/skaters_1.csv"
df = load_nhl_data(path)

def init_data_handler(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")
    df = load_nhl_data(path)
    if df is None:
        raise ValueError("Échec du chargement des données NHL.")
    return df

def rechercher_donnees(column, value):
    if df is None:
        raise RuntimeError("Données NHL non initialisées.")
    if column not in df.columns:
        raise KeyError(f"Colonne '{column}' introuvable.")
    return df[df[column].str.contains(value, case=False, na=False)]

def obtenir_classement(criterion, ascending=False):
    if df is None:
        raise RuntimeError("Données NHL non initialisées.")
    if criterion not in df.columns:
        raise KeyError(f"Critère '{criterion}' introuvable.")
    return df.sort_values(by=criterion, ascending=ascending)
