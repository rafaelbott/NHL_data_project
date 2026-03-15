import pandas as pd
#file_path = r"donnes/skaters_1.csv"


def load_nhl_data(file_path):
    """
    Charge un fichier CSV contenant les statistiques des joueurs de la NHL en ne gardant que les lignes où situation = 'all'.
    
    :param file_path: Chemin du fichier CSV
    :return: DataFrame contenant les données filtrées
    """
    try:
        df = pd.read_csv(file_path)
        
        # Filtrer uniquement les lignes où situation est 'all'
        df = df[df["situation"] == "all"].copy()
        
        # Extraction des colonnes nécessaires
        columns_to_extract = ["playerId", "name", "team", "games_played", "I_F_goals", "I_F_primaryAssists", "I_F_secondaryAssists", "I_F_points"]
        existing_columns = [col for col in columns_to_extract if col in df.columns]
        
        if not existing_columns:
            raise ValueError("Aucune des colonnes requises n'est présente dans le fichier.")
        
        df_filtered = df[existing_columns].copy()
        
        # Création de la colonne I_F_Assists en additionnant les colonnes primary et secondary assists
        if "I_F_primaryAssists" in df_filtered.columns and "I_F_secondaryAssists" in df_filtered.columns:
            df_filtered["I_F_assists"] = df_filtered["I_F_primaryAssists"] + df_filtered["I_F_secondaryAssists"]
        else:
            raise ValueError("Les colonnes 'I_F_primaryAssists' et/ou 'I_F_secondaryAssists' sont manquantes.")
        
        # Modifier l'index avec le prénom et l'ID du joueur
        df_filtered.loc[:, "display_name"] = df_filtered["name"] + " (" + df_filtered["playerId"].astype(str) + ")"
        # Supprimer les colonnes inutiles après modification
        df_filtered = df_filtered.drop(columns=["playerId", "name"])
        
        return df_filtered
    
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return None
