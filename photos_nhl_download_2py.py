import pandas as pd
import requests
import os
from PIL import Image

# Chemins du CSV et du dossier de destination
csv_path = r"C:/Users/anton/OneDrive/Bureau/code/nsi_hockey/3/donnes/skaters_1.csv"
dest_dir = r"C:/Users/anton/OneDrive/Bureau/code/nsi_hockey/3/donnes/"

# Colonnes attendues: playerId et team (code équipe, ex: PIT, NYR, etc)
df = pd.read_csv(csv_path)
os.makedirs(dest_dir, exist_ok=True)

# Vérification colonne 'team'
if 'team' not in df.columns or 'playerId' not in df.columns:
    raise Exception("Le CSV doit contenir les colonnes 'playerId' et 'team'.")

for _, row in df.iterrows():
    pid = str(row['playerId'])
    team = str(row['team']).strip().upper()
    url = f"https://assets.nhle.com/mugs/nhl/20242025/{team}/{pid}.png"
    dest = os.path.join(dest_dir, f"{pid}.png")
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200 and r.headers.get('Content-Type', '').startswith('image'):
            with open(dest, "wb") as f:
                f.write(r.content)
            print(f"Téléchargé {pid} ({team})")
        else:
            Image.new("RGB", (168, 168), color="gray").save(dest)
            print(f"Photo absente ou inaccessible pour {pid} ({team})")
    except Exception as e:
        Image.new("RGB", (168, 168), color="gray").save(dest)
        print(f"Erreur pour {pid} ({team}): {e}")

print(f"Terminé ! Images dans {dest_dir}")