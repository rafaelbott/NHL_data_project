# Importation d'une bibliothèque Python
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
# Importation d'une bibliothèque Python
import nhl_data_handler25
# Importation d'une bibliothèque Python
import os
# Importation d'une bibliothèque Python
import random
from PIL import Image, ImageTk
# Importation d'une bibliothèque Python
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Importation d'une bibliothèque Python
import matplotlib
# Importation d'une bibliothèque Python
import numpy as np
# Importation d'une bibliothèque Python
import pandas as pd
matplotlib.use('TkAgg')

# Définition des couleurs et chemins de fichiers pour la bio des joueurs et images
# Affectation d'une valeur à une variable
COULEUR_BLEU_CIEL = "#87CEEB"
# Affectation d'une valeur à une variable
CHEMIN_BIO_EXCEL = r"donnes/skaters_bio_1.xlsx"
# Affectation d'une valeur à une variable
IMAGES_FOLDER = r"donnes" 

# Chargement du fichier Excel de biographie des joueurs
try:
# Affectation d'une valeur à une variable
    _raw = pd.read_excel(CHEMIN_BIO_EXCEL, engine='openpyxl')
# Affectation d'une valeur à une variable
    col0 = _raw.columns[0]
# Affectation d'une valeur à une variable
    headers = col0.split(',')
# Affectation d'une valeur à une variable
    df_bio = _raw[col0].str.split(',', n=len(headers) - 1, expand=True)
# Affectation d'une valeur à une variable
    df_bio.columns = headers
# Affectation d'une valeur à une variable
    df_bio = df_bio.applymap(lambda x: x.strip().strip('"') if isinstance(x, str) else x)
except Exception as e:
    # En cas d'erreur, on crée un DataFrame vide avec les colonnes attendues
# Affectation d'une valeur à une variable
    df_bio = pd.DataFrame(columns=[
        "playerId", "name", "age", "lieu_naissance",
        "date_naissance", "historique_equipe", "photo"
    ])
# Affiche un message à l'écran
    print(f"Impossible de charger skaters_bio.xlsx : {e}")

# Chargement des données principales des joueurs depuis un CSV
# Affectation d'une valeur à une variable
file_path = r"donnes/skaters_1.csv"
try:
# Affectation d'une valeur à une variable
    data = nhl_data_handler25.init_data_handler(file_path)
except Exception as e:
    tk.Tk().withdraw()
    messagebox.showerror("Erreur de chargement", str(e))
# Affectation d'une valeur à une variable
    data = None

# Définition d'une fonction
def afficher_statistiques():
    #Affiche les statistiques NHL dans une nouvelle fenêtre (tableau triable et biographie au double-clic).
# Condition : si cette condition est vraie, on exécute ce bloc
    if data is None:
# Renvoie une valeur depuis une fonction
        return
# Affectation d'une valeur à une variable
    fen = tk.Toplevel(root)
    fen.title("Statistiques NHL Chargées")
# Affectation d'une valeur à une variable
    fen.configure(bg=COULEUR_BLEU_CIEL)
    fen.geometry("1200x600")
# Affectation d'une valeur à une variable
    frame = tk.Frame(fen, bg=COULEUR_BLEU_CIEL)
# Affectation d'une valeur à une variable
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
# Affectation d'une valeur à une variable
    style = ttk.Style()
# Affectation d'une valeur à une variable
    style.configure("Treeview", background="#E8E8E8", foreground="black", rowheight=25, fieldbackground="#E8E8E8")
# Affectation d'une valeur à une variable
    style.map('Treeview', background=[('selected', '#0066CC')])
# Affectation d'une valeur à une variable
    columns = list(data.columns)
# Affectation d'une valeur à une variable
    tree_frame = tk.Frame(frame)
# Affectation d'une valeur à une variable
    tree_frame.pack(fill=tk.BOTH, expand=True)
# Affectation d'une valeur à une variable
    tree_scroll_y = tk.Scrollbar(tree_frame)
# Affectation d'une valeur à une variable
    tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
# Affectation d'une valeur à une variable
    tree_scroll_x = tk.Scrollbar(tree_frame, orient='horizontal')
# Affectation d'une valeur à une variable
    tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
# Affectation d'une valeur à une variable
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
# Affectation d'une valeur à une variable
                        yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
# Affectation d'une valeur à une variable
    tree_scroll_y.config(command=tree.yview)
# Affectation d'une valeur à une variable
    tree_scroll_x.config(command=tree.xview)

    # Création des en-têtes de colonnes et ajustement de largeur
# Boucle for : permet de répéter une action plusieurs fois
    for col in columns:
# Affectation d'une valeur à une variable
        tree.heading(col, text=col, command=lambda c=col: trier_treeview(tree, c, False))
# Condition : si cette condition est vraie, on exécute ce bloc
        if col == "display_name" or col == "team":
# Affectation d'une valeur à une variable
            tree.column(col, width=200, minwidth=150)
# Sinon : ce bloc s'exécute si aucune condition précédente n'est vraie
        else:
# Affectation d'une valeur à une variable
            tree.column(col, width=100, minwidth=80)
# Affectation d'une valeur à une variable
    player_ids = {}
# Boucle for : permet de répéter une action plusieurs fois
    for i, row in data.iterrows():
# Affectation d'une valeur à une variable
        values = [row[col] for col in columns]
# Affectation d'une valeur à une variable
        item_id = tree.insert('', tk.END, values=values)
# Affectation d'une valeur à une variable
        player_name = row['display_name'] if 'display_name' in row else "Inconnu"
# Affectation d'une valeur à une variable
        player_ids[item_id] = player_name
# Affectation d'une valeur à une variable
    tree.pack(fill=tk.BOTH, expand=True)

# Définition d'une fonction
    def afficher_biographie(event):
        #Affiche une fiche biographique détaillée du joueur au double-clic sur une ligne.
# Affectation d'une valeur à une variable
        item = tree.identify('item', event.x, event.y)
# Condition : si cette condition est vraie, on exécute ce bloc
        if not item:
# Renvoie une valeur depuis une fonction
            return

# Affectation d'une valeur à une variable
        player_name = player_ids[item]
# Affectation d'une valeur à une variable
        nom_joueur = player_name.split(" (")[0] if " (" in player_name else player_name

        row = df_bio[df_bio["name"].str.strip().str.lower() == nom_joueur.strip().lower()]
# Condition : si cette condition est vraie, on exécute ce bloc
        if row.empty:
            messagebox.showinfo("Biographie", f"Aucune fiche biographique trouvée pour « {nom_joueur} ».")
# Renvoie une valeur depuis une fonction
            return

# Affectation d'une valeur à une variable
        info = row.iloc[0]
# Affectation d'une valeur à une variable
        age = info.get("age", "N/A")
# Affectation d'une valeur à une variable
        lieu = info.get("lieu_naissance", "N/A")
# Affectation d'une valeur à une variable
        date_naiss = info.get("date_naissance", "N/A")
# Affectation d'une valeur à une variable
        historique = info.get("historique_equipe", "N/A")

# Affectation d'une valeur à une variable
        bio_window = tk.Toplevel(fen)
        bio_window.title(f"Biographie de {nom_joueur}")
# Affectation d'une valeur à une variable
        bio_window.configure(bg="#FFFFFF")
        bio_window.geometry("800x600")

# Affectation d'une valeur à une variable
        main_frame = tk.Frame(bio_window, bg="#FFFFFF")
# Affectation d'une valeur à une variable
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Affichage de la photo du joueur ou d'un placeholder
# Affectation d'une valeur à une variable
        photo_frame = tk.Frame(main_frame, bg="#FFFFFF", width=300)
# Affectation d'une valeur à une variable
        photo_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
# Affectation d'une valeur à une variable
        photo_placeholder = tk.Canvas(photo_frame, width=250, height=300, bg="#DDDDDD")
# Affectation d'une valeur à une variable
        photo_placeholder.pack(pady=10)
# Affectation d'une valeur à une variable
        photo_placeholder.create_rectangle(10, 10, 240, 290, outline="#999999", width=2)
        try:
# Affectation d'une valeur à une variable
            player_id = str(info.get("playerId", "")).strip()
# Affectation d'une valeur à une variable
            image_path = os.path.join(IMAGES_FOLDER, f"{player_id}.jpg")
# Condition : si cette condition est vraie, on exécute ce bloc
            if not os.path.exists(image_path):
# Affectation d'une valeur à une variable
                image_path = os.path.join(IMAGES_FOLDER, f"{player_id}.png")
# Affiche un message à l'écran
            print("Recherche image:", image_path)
# Condition : si cette condition est vraie, on exécute ce bloc
            if os.path.exists(image_path):
# Affectation d'une valeur à une variable
                image = Image.open(image_path)
# Affectation d'une valeur à une variable
                image = image.resize((250, 300), Image.LANCZOS)
# Affectation d'une valeur à une variable
                photo = ImageTk.PhotoImage(image)
                # Affiche l'image dans le canvas, centré
# Affectation d'une valeur à une variable
                photo_placeholder.create_image(125, 150, image=photo, anchor="center")
# Affectation d'une valeur à une variable
                photo_placeholder.photo = photo  # Important pour garder la référence à l'image
# Sinon : ce bloc s'exécute si aucune condition précédente n'est vraie
            else:
# Affectation d'une valeur à une variable
                photo_placeholder.create_text(125, 150, text="Photo du joueur\nnon disponible", font=('Arial', 12), fill="#666666")
        except Exception as e:
# Affectation d'une valeur à une variable
            photo_placeholder.create_text(125, 150, text="Erreur image", font=('Arial', 12), fill="#FF0000")
# Affiche un message à l'écran
            print(f"Erreur lors de l'affichage de la photo : {e}")

        # Affichage des infos biographiques et stats
# Affectation d'une valeur à une variable
        info_frame = tk.Frame(main_frame, bg="#FFFFFF")
# Affectation d'une valeur à une variable
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Affectation d'une valeur à une variable
        tk.Label(info_frame, text=nom_joueur, font=('Arial', 18, 'bold'), bg="#FFFFFF", fg="#0066CC").pack(anchor='w', pady=(0, 20))
# Affectation d'une valeur à une variable
        tk.Label(info_frame, text=f"Âge : {age} ans", font=('Arial', 12), bg="#FFFFFF", anchor='w').pack(anchor='w', pady=5)
# Affectation d'une valeur à une variable
        tk.Label(info_frame, text=f"Né le : {date_naiss}", font=('Arial', 12), bg="#FFFFFF", anchor='w').pack(anchor='w', pady=5)
# Affectation d'une valeur à une variable
        tk.Label(info_frame, text=f"Lieu de naissance : {lieu}", font=('Arial', 12), bg="#FFFFFF", anchor='w').pack(anchor='w', pady=5)

# Affectation d'une valeur à une variable
        tk.Label(info_frame, text="Equipes les plus marquantes :", font=('Arial', 14, 'bold'), bg="#FFFFFF", fg="#0066CC").pack(anchor='w', pady=(20, 10))
# Boucle for : permet de répéter une action plusieurs fois
        for ligne in str(historique).split(';'):
# Affectation d'une valeur à une variable
            tk.Label(info_frame, text=f"• {ligne.strip()}", font=('Arial', 12), bg="#FFFFFF", anchor='w').pack(anchor='w', pady=3)

# Affectation d'une valeur à une variable
        tk.Label(info_frame, text="Statistiques actuelles :", font=('Arial', 14, 'bold'), bg="#FFFFFF", fg="#0066CC").pack(anchor='w', pady=(20, 10))
# Affectation d'une valeur à une variable
        selected_values = tree.item(item, 'values')
# Condition : si cette condition est vraie, on exécute ce bloc
        if selected_values:
# Affectation d'une valeur à une variable
            stats_frame = tk.Frame(info_frame, bg="#FFFFFF")
# Affectation d'une valeur à une variable
            stats_frame.pack(anchor='w', fill=tk.X, pady=5)
            try:
# Affectation d'une valeur à une variable
                cols = list(data.columns)
# Affectation d'une valeur à une variable
                team_idx = cols.index("team") if "team" in cols else -1
# Affectation d'une valeur à une variable
                games_idx = cols.index("games_played") if "games_played" in cols else -1
# Affectation d'une valeur à une variable
                goals_idx = cols.index("I_F_goals") if "I_F_goals" in cols else -1
# Affectation d'une valeur à une variable
                assists_idx = cols.index("I_F_assists") if "I_F_assists" in cols else -1
# Affectation d'une valeur à une variable
                points_idx = cols.index("I_F_points") if "I_F_points" in cols else -1

# Condition : si cette condition est vraie, on exécute ce bloc
                if team_idx >= 0:
# Affectation d'une valeur à une variable
                    tk.Label(stats_frame, text=f"Équipe actuelle : {selected_values[team_idx]}", font=('Arial', 12), bg="#FFFFFF").pack(anchor='w', pady=2)
# Condition : si cette condition est vraie, on exécute ce bloc
                if games_idx >= 0:
# Affectation d'une valeur à une variable
                    tk.Label(stats_frame, text=f"Matchs joués : {selected_values[games_idx]}", font=('Arial', 12), bg="#FFFFFF").pack(anchor='w', pady=2)
# Condition : si cette condition est vraie, on exécute ce bloc
                if goals_idx >= 0:
# Affectation d'une valeur à une variable
                    tk.Label(stats_frame, text=f"Buts : {selected_values[goals_idx]}", font=('Arial', 12), bg="#FFFFFF").pack(anchor='w', pady=2)
# Condition : si cette condition est vraie, on exécute ce bloc
                if assists_idx >= 0:
# Affectation d'une valeur à une variable
                    tk.Label(stats_frame, text=f"Passes décisives : {selected_values[assists_idx]}", font=('Arial', 12), bg="#FFFFFF").pack(anchor='w', pady=2)
# Condition : si cette condition est vraie, on exécute ce bloc
                if points_idx >= 0:
# Affectation d'une valeur à une variable
                    tk.Label(stats_frame, text=f"Points : {selected_values[points_idx]}", font=('Arial', 12), bg="#FFFFFF").pack(anchor='w', pady=2)
            except Exception as e:
# Affiche un message à l'écran
                print(f"Erreur lors de l'affichage des statistiques : {e}")

    tree.bind("<Double-1>", afficher_biographie)

# Définition d'une fonction
    def trier_treeview(tv, col, reverse):
        #Trie les lignes du TreeView selon la colonne cliquée.
# Affectation d'une valeur à une variable
        data_list = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
# Affectation d'une valeur à une variable
            data_list.sort(key=lambda x: float(x[0]), reverse=reverse)
        except ValueError:
# Affectation d'une valeur à une variable
            data_list.sort(reverse=reverse)
# Boucle for : permet de répéter une action plusieurs fois
        for index, (val, k) in enumerate(data_list):
            tv.move(k, '', index)
# Affectation d'une valeur à une variable
        tv.heading(col, command=lambda: trier_treeview(tv, col, not reverse))

    tk.Label(frame,
# Affectation d'une valeur à une variable
             text="Cliquez sur les en-têtes des colonnes pour trier les données. Recherche rapide avec le ticker de l'équipe ou le nom ou prénom du joueur. Double-cliquez sur un joueur pour voir sa biographie.",
# Affectation d'une valeur à une variable
             bg=COULEUR_BLEU_CIEL, font=('Arial', 9), fg="#333333").pack(pady=5)

    # Zone de recherche rapide
# Affectation d'une valeur à une variable
    search_frame = tk.Frame(frame, bg=COULEUR_BLEU_CIEL)
# Affectation d'une valeur à une variable
    search_frame.pack(fill=tk.X, padx=5, pady=5)

# Affectation d'une valeur à une variable
    tk.Label(search_frame, text="Recherche rapide:", bg=COULEUR_BLEU_CIEL).pack(side=tk.LEFT, padx=5)
# Affectation d'une valeur à une variable
    search_entry = tk.Entry(search_frame, width=30)
# Affectation d'une valeur à une variable
    search_entry.pack(side=tk.LEFT, padx=5)

# Définition d'une fonction
    def recherche_rapide():
        """Recherche sur toutes les colonnes et réaffiche un sous-ensemble des lignes."""
# Affectation d'une valeur à une variable
        query = search_entry.get().lower()
# Boucle for : permet de répéter une action plusieurs fois
        for item in tree.get_children():
            tree.delete(item)
        player_ids.clear()
# Boucle for : permet de répéter une action plusieurs fois
        for i, row in data.iterrows():
# Condition : si cette condition est vraie, on exécute ce bloc
            if any(str(row[col]).lower().find(query) != -1 for col in columns):
# Affectation d'une valeur à une variable
                values = [row[col] for col in columns]
# Affectation d'une valeur à une variable
                item_id = tree.insert('', tk.END, values=values)
# Affectation d'une valeur à une variable
                player_name = row['display_name'] if 'display_name' in row else "Inconnu"
# Affectation d'une valeur à une variable
                player_ids[item_id] = player_name

# Affectation d'une valeur à une variable
    tk.Button(search_frame, text="Rechercher", command=recherche_rapide, bg="#0066CC", fg="white").pack(side=tk.LEFT, padx=5)
# Affectation d'une valeur à une variable
    tk.Button(search_frame, text="Réinitialiser", command=lambda: [search_entry.delete(0, tk.END), recherche_rapide()], bg="#CC0000", fg="white").pack(side=tk.LEFT, padx=5)

# Définition d'une fonction
def ouvrir_recherche():
    #Permet de rechercher un joueur ou une équipe (affichage texte).
# Condition : si cette condition est vraie, on exécute ce bloc
    if data is None:
# Renvoie une valeur depuis une fonction
        return
# Affectation d'une valeur à une variable
    fen = tk.Toplevel(root)
    fen.title("Recherche de Joueur ou Équipe")
# Affectation d'une valeur à une variable
    fen.configure(bg=COULEUR_BLEU_CIEL)
# Affectation d'une valeur à une variable
    frame = tk.Frame(fen, bg=COULEUR_BLEU_CIEL, padx=10, pady=10)
# Affectation d'une valeur à une variable
    frame.pack(fill=tk.BOTH, expand=True)

# Affectation d'une valeur à une variable
    tk.Label(frame, text="Choisissez le type de recherche :", bg=COULEUR_BLEU_CIEL, font=('Arial', 11, 'bold')).pack(pady=5)
# Affectation d'une valeur à une variable
    type_var = tk.StringVar(value="display_name")
# Affectation d'une valeur à une variable
    tk.Radiobutton(frame, text="Joueur", variable=type_var, value="display_name", bg=COULEUR_BLEU_CIEL).pack()
# Affectation d'une valeur à une variable
    tk.Radiobutton(frame, text="Équipe", variable=type_var, value="team", bg=COULEUR_BLEU_CIEL).pack()

# Affectation d'une valeur à une variable
    tk.Label(frame, text="Entrez la valeur recherchée :", bg=COULEUR_BLEU_CIEL, font=('Arial', 11, 'bold')).pack(pady=5)
# Affectation d'une valeur à une variable
    ent = tk.Entry(frame, width=30)
    ent.pack()

# Affectation d'une valeur à une variable
    res = scrolledtext.ScrolledText(frame, width=100, height=20)
# Affectation d'une valeur à une variable
    res.pack(pady=5)

# Définition d'une fonction
    def do_search():
        #Lance la recherche via le module handler puis affiche le résultat.
# Affectation d'une valeur à une variable
        col, val = type_var.get(), ent.get().strip()
# Condition : si cette condition est vraie, on exécute ce bloc
        if not val:
            messagebox.showwarning("Attention", "Veuillez saisir une valeur.")
# Renvoie une valeur depuis une fonction
            return
        try:
# Affectation d'une valeur à une variable
            df_res = nhl_data_handler25.rechercher_donnees(col, val)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
# Renvoie une valeur depuis une fonction
            return
        res.delete("1.0", tk.END)
# Affectation d'une valeur à une variable
        res.insert(tk.END, df_res.to_string(index=False) if not df_res.empty else "Aucune correspondance trouvée.")

# Affectation d'une valeur à une variable
    tk.Button(frame, text="Rechercher", command=do_search, bg="#0066CC", fg="white", font=('Arial', 10, 'bold')).pack(pady=5)

# Définition d'une fonction
def ouvrir_classement():
    #Affiche un classement des joueurs selon un critère choisi.
# Affectation d'une valeur à une variable
    fen = tk.Toplevel(root)
    fen.title("Classement des Joueurs")
# Affectation d'une valeur à une variable
    fen.configure(bg=COULEUR_BLEU_CIEL)
# Affectation d'une valeur à une variable
    frame = tk.Frame(fen, bg=COULEUR_BLEU_CIEL, padx=10, pady=10)
# Affectation d'une valeur à une variable
    frame.pack(fill=tk.BOTH, expand=True)

# Affectation d'une valeur à une variable
    tk.Label(frame, text="Choisissez le critère de classement :", bg=COULEUR_BLEU_CIEL, font=('Arial', 11, 'bold')).pack(pady=5)
# Affectation d'une valeur à une variable
    crits = ["I_F_goals", "I_F_assists", "I_F_points"]
# Affectation d'une valeur à une variable
    crit_var = tk.StringVar(value=crits[0])
# Affectation d'une valeur à une variable
    ttk.Combobox(frame, textvariable=crit_var, values=crits, state="readonly").pack(pady=5)

# Affectation d'une valeur à une variable
    tk.Label(frame, text="Ordre de classement :", bg=COULEUR_BLEU_CIEL, font=('Arial', 11, 'bold')).pack(pady=5)
# Affectation d'une valeur à une variable
    ordre_var = tk.StringVar(value="Descendant")
# Affectation d'une valeur à une variable
    tk.Radiobutton(frame, text="Descendant", variable=ordre_var, value="Descendant", bg=COULEUR_BLEU_CIEL).pack()
# Affectation d'une valeur à une variable
    tk.Radiobutton(frame, text="Ascendant", variable=ordre_var, value="Ascendant", bg=COULEUR_BLEU_CIEL).pack()

# Affectation d'une valeur à une variable
    res = scrolledtext.ScrolledText(frame, width=100, height=20)
# Affectation d'une valeur à une variable
    res.pack(pady=5)

# Définition d'une fonction
    def do_rank():
        #Affiche le top 10 selon le classement choisi.
        crit, asc = crit_var.get(), (ordre_var.get() == "Ascendant")
        try:
# Affectation d'une valeur à une variable
            df_rank = nhl_data_handler25.obtenir_classement(crit, ascending=asc).head(10)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
# Renvoie une valeur depuis une fonction
            return
        res.delete("1.0", tk.END)
# Affectation d'une valeur à une variable
        res.insert(tk.END, df_rank.to_string(index=False))

# Affectation d'une valeur à une variable
    tk.Button(frame, text="Afficher le classement", command=do_rank, bg="#0066CC", fg="white", font=('Arial', 10, 'bold')).pack(pady=5)

# Définition d'une fonction
def afficher_joueurs_aleatoires():
    #Affiche 10 joueurs sélectionnés aléatoirement.
# Condition : si cette condition est vraie, on exécute ce bloc
    if data is None:
# Renvoie une valeur depuis une fonction
        return
# Affectation d'une valeur à une variable
    fen = tk.Toplevel(root)
    fen.title("10 Joueurs Aléatoires")
# Affectation d'une valeur à une variable
    fen.configure(bg=COULEUR_BLEU_CIEL)
# Affectation d'une valeur à une variable
    frame = tk.Frame(fen, bg=COULEUR_BLEU_CIEL, padx=10, pady=10)
# Affectation d'une valeur à une variable
    frame.pack(fill=tk.BOTH, expand=True)

# Affectation d'une valeur à une variable
    tk.Label(frame, text="10 Joueurs Aléatoires", bg=COULEUR_BLEU_CIEL, font=('Arial', 14, 'bold'), fg="#0066CC").pack(pady=10)
# Affectation d'une valeur à une variable
    res = scrolledtext.ScrolledText(frame, width=100, height=20)
# Affectation d'une valeur à une variable
    res.pack(pady=5)

# Définition d'une fonction
    def generer_aleatoire():
        #Génère et affiche 10 joueurs différents à chaque clic.
        try:
# Affectation d'une valeur à une variable
            total_joueurs = len(data)
# Condition : si cette condition est vraie, on exécute ce bloc
            if total_joueurs < 10:
                messagebox.showwarning("Attention", f"Il n'y a que {total_joueurs} joueurs disponibles.")
# Affectation d'une valeur à une variable
                indices = list(range(total_joueurs))
# Sinon : ce bloc s'exécute si aucune condition précédente n'est vraie
            else:
# Affectation d'une valeur à une variable
                indices = random.sample(range(total_joueurs), 10)
# Affectation d'une valeur à une variable
            joueurs_aleatoires = data.iloc[indices].copy()
            res.delete("1.0", tk.END)
# Affectation d'une valeur à une variable
            res.insert(tk.END, joueurs_aleatoires.to_string(index=False))
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

# Affectation d'une valeur à une variable
    tk.Button(frame, text="Générer de nouveaux joueurs aléatoires", command=generer_aleatoire, bg="#0066CC", fg="white", font=('Arial', 10, 'bold')).pack(pady=10)
    generer_aleatoire()

# Définition d'une fonction
def ouvrir_comparaison_graphique():
    #Affiche une interface de sélection de joueurs pour comparaison graphique (radar ou barres).
# Condition : si cette condition est vraie, on exécute ce bloc
    if data is None:
# Renvoie une valeur depuis une fonction
        return
# Affectation d'une valeur à une variable
    fen = tk.Toplevel(root)
    fen.title("Comparaison Graphique des Joueurs")
# Affectation d'une valeur à une variable
    fen.configure(bg=COULEUR_BLEU_CIEL)
    fen.geometry("1200x800")
# Affectation d'une valeur à une variable
    main_frame = tk.Frame(fen, bg=COULEUR_BLEU_CIEL, padx=10, pady=10)
# Affectation d'une valeur à une variable
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Interface de sélection de joueurs
# Affectation d'une valeur à une variable
    control_frame = tk.Frame(main_frame, bg=COULEUR_BLEU_CIEL, width=300)
# Affectation d'une valeur à une variable
    control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

# Affectation d'une valeur à une variable
    tk.Label(control_frame, text="Sélection des Joueurs", font=('Arial', 14, 'bold'), bg=COULEUR_BLEU_CIEL, fg="#0066CC").pack(pady=(0, 20))

# Affectation d'une valeur à une variable
    tk.Label(control_frame, text="Rechercher un joueur:", bg=COULEUR_BLEU_CIEL).pack(anchor='w')
# Affectation d'une valeur à une variable
    search_var = tk.StringVar()
# Affectation d'une valeur à une variable
    search_entry = tk.Entry(control_frame, textvariable=search_var, width=25)
# Affectation d'une valeur à une variable
    search_entry.pack(fill=tk.X, pady=(0, 10))

# Affectation d'une valeur à une variable
    tk.Label(control_frame, text="Résultats de la recherche:", bg=COULEUR_BLEU_CIEL).pack(anchor='w')
# Affectation d'une valeur à une variable
    search_results_frame = tk.Frame(control_frame)
# Affectation d'une valeur à une variable
    search_results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

# Affectation d'une valeur à une variable
    search_results_listbox = tk.Listbox(search_results_frame, width=30, height=10)
# Affectation d'une valeur à une variable
    search_results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Affectation d'une valeur à une variable
    search_scrollbar = tk.Scrollbar(search_results_frame, orient="vertical", command=search_results_listbox.yview)
# Affectation d'une valeur à une variable
    search_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# Affectation d'une valeur à une variable
    search_results_listbox.config(yscrollcommand=search_scrollbar.set)

# Affectation d'une valeur à une variable
    tk.Label(control_frame, text="Joueurs sélectionnés:", bg=COULEUR_BLEU_CIEL).pack(anchor='w', pady=(10, 0))
# Affectation d'une valeur à une variable
    selected_players_frame = tk.Frame(control_frame)
# Affectation d'une valeur à une variable
    selected_players_frame.pack(fill=tk.BOTH, expand=True, pady=5)

# Affectation d'une valeur à une variable
    selected_players_listbox = tk.Listbox(selected_players_frame, width=30, height=5)
# Affectation d'une valeur à une variable
    selected_players_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Affectation d'une valeur à une variable
    selected_scrollbar = tk.Scrollbar(selected_players_frame, orient="vertical", command=selected_players_listbox.yview)
# Affectation d'une valeur à une variable
    selected_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# Affectation d'une valeur à une variable
    selected_players_listbox.config(yscrollcommand=selected_scrollbar.set)

# Affectation d'une valeur à une variable
    search_results = []
# Affectation d'une valeur à une variable
    selected_players = []
# Affectation d'une valeur à une variable
    graph_type_radar = [True]  # Liste pour mutabilité

# Affectation d'une valeur à une variable
    buttons_frame = tk.Frame(control_frame, bg=COULEUR_BLEU_CIEL)
# Affectation d'une valeur à une variable
    buttons_frame.pack(fill=tk.X, pady=10)

# Affectation d'une valeur à une variable
    graph_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10)
# Affectation d'une valeur à une variable
    graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Définition d'une fonction
    def rechercher_joueurs():
        #Recherche de joueurs selon le nom tapé, maj la liste de résultats.
        search_results_listbox.delete(0, tk.END)
# Affectation d'une valeur à une variable
        terme_recherche = search_var.get().lower().strip()
# Condition : si cette condition est vraie, on exécute ce bloc
        if not terme_recherche:
# Renvoie une valeur depuis une fonction
            return
# Affectation d'une valeur à une variable
        resultats = data[data['display_name'].str.lower().str.contains(terme_recherche)]
# Boucle for : permet de répéter une action plusieurs fois
        for _, row in resultats.iterrows():
# Affectation d'une valeur à une variable
            nom_joueur = row['display_name']
            search_results_listbox.insert(tk.END, nom_joueur)
        nonlocal search_results
# Affectation d'une valeur à une variable
        search_results = list(resultats['display_name'])

# Définition d'une fonction
    def ajouter_joueur():
        #Ajoute un joueur à la sélection pour le graphique (max 5).
# Affectation d'une valeur à une variable
        selection = search_results_listbox.curselection()
# Condition : si cette condition est vraie, on exécute ce bloc
        if not selection:
# Renvoie une valeur depuis une fonction
            return
# Condition : si cette condition est vraie, on exécute ce bloc
        if len(selected_players) >= 5:
            messagebox.showwarning("Limite atteinte", "Vous ne pouvez pas sélectionner plus de 5 joueurs à la fois.")
# Renvoie une valeur depuis une fonction
            return
# Affectation d'une valeur à une variable
        nom_joueur = search_results_listbox.get(selection[0])
# Condition : si cette condition est vraie, on exécute ce bloc
        if nom_joueur in selected_players:
# Renvoie une valeur depuis une fonction
            return
        selected_players_listbox.insert(tk.END, nom_joueur)
        selected_players.append(nom_joueur)
        mettre_a_jour_graphique()

# Définition d'une fonction
    def retirer_joueur():
        #Retire un joueur de la sélection graphique.
# Affectation d'une valeur à une variable
        selection = selected_players_listbox.curselection()
# Condition : si cette condition est vraie, on exécute ce bloc
        if not selection:
# Renvoie une valeur depuis une fonction
            return
# Affectation d'une valeur à une variable
        idx = selection[0]
# Affectation d'une valeur à une variable
        nom_joueur = selected_players_listbox.get(idx)
        selected_players_listbox.delete(idx)
        selected_players.remove(nom_joueur)
        mettre_a_jour_graphique()

# Définition d'une fonction
    def switch_graph_type():
        #Change le type de graphique (radar/barres).
# Affectation d'une valeur à une variable
        graph_type_radar[0] = not graph_type_radar[0]
        mettre_a_jour_graphique()

# Définition d'une fonction
    def mettre_a_jour_graphique():
        #Affiche le graphique pour les joueurs sélectionnés.
# Boucle for : permet de répéter une action plusieurs fois
        for widget in graph_frame.winfo_children():
            widget.destroy()
# Condition : si cette condition est vraie, on exécute ce bloc
        if not selected_players:
# Affectation d'une valeur à une variable
            tk.Label(graph_frame, text="Sélectionnez des joueurs pour afficher leurs statistiques", bg="white", font=('Arial', 12)).pack(expand=True)
# Renvoie une valeur depuis une fonction
            return
# Affectation d'une valeur à une variable
        stats = ['I_F_goals', 'I_F_assists', 'I_F_points', 'games_played']
# Affectation d'une valeur à une variable
        stats_labels = ['Buts', 'Passes', 'Points', 'Matchs joués']
# Affectation d'une valeur à une variable
        colors = ['#FF4500', '#1E90FF', '#32CD32', '#FFD700', '#9932CC']
# Affectation d'une valeur à une variable
        joueurs_data = []
# Boucle for : permet de répéter une action plusieurs fois
        for nom in selected_players:
            row = data[data['display_name'] == nom]
# Condition : si cette condition est vraie, on exécute ce bloc
            if row.empty:
                continue
# Affectation d'une valeur à une variable
            row = row.iloc[0]
            joueurs_data.append([float(row[stat]) if not pd.isnull(row[stat]) else 0 for stat in stats])
# Condition : si cette condition est vraie, on exécute ce bloc
        if not joueurs_data:
# Affectation d'une valeur à une variable
            tk.Label(graph_frame, text="Erreur : joueurs introuvables dans les données.", bg="white", fg="red").pack(expand=True)
# Renvoie une valeur depuis une fonction
            return
# Condition : si cette condition est vraie, on exécute ce bloc
        if graph_type_radar[0]:
            # Graphique radar
# Affectation d'une valeur à une variable
            fig = plt.figure(figsize=(8, 6))
# Affectation d'une valeur à une variable
            ax = fig.add_subplot(111, polar=True)
# Affectation d'une valeur à une variable
            N = len(stats)
# Affectation d'une valeur à une variable
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
# Affectation d'une valeur à une variable
            angles += angles[:1]
# Boucle for : permet de répéter une action plusieurs fois
            for i, (nom, values) in enumerate(zip(selected_players, joueurs_data)):
# Affectation d'une valeur à une variable
                val = values + [values[0]]
# Affectation d'une valeur à une variable
                ax.plot(angles, val, linewidth=2, linestyle='solid', label=nom, color=colors[i % len(colors)])
# Affectation d'une valeur à une variable
                ax.fill(angles, val, alpha=0.1, color=colors[i % len(colors)])
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(stats_labels)
# Affectation d'une valeur à une variable
            ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
# Affectation d'une valeur à une variable
            plt.title("Comparaison des Statistiques des Joueurs (Radar)", size=15, color='#333333', y=1.1)
# Sinon : ce bloc s'exécute si aucune condition précédente n'est vraie
        else:
            # Graphique barres
# Affectation d'une valeur à une variable
            fig, ax = plt.subplots(figsize=(10, 6))
# Affectation d'une valeur à une variable
            bar_width = 0.15
# Affectation d'une valeur à une variable
            indices = np.arange(len(stats))
# Boucle for : permet de répéter une action plusieurs fois
            for i, (nom, values) in enumerate(zip(selected_players, joueurs_data)):
# Affectation d'une valeur à une variable
                ax.bar(indices + i * bar_width, values, bar_width, label=nom, color=colors[i % len(colors)])
            ax.set_xticks(indices + bar_width * (len(selected_players)-1) / 2)
            ax.set_xticklabels(stats_labels)
            ax.legend()
# Affectation d'une valeur à une variable
            plt.title("Comparaison des Statistiques des Joueurs (Barres)", size=15, color='#333333')
        plt.tight_layout()
# Affectation d'une valeur à une variable
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
# Affectation d'une valeur à une variable
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Définition d'une fonction
    def analyse_selection():
        #Ouvre une analyse avancée pour les joueurs sélectionnés.
# Affectation d'une valeur à une variable
        noms = list(selected_players)
        analyse_avancee_joueurs(noms, data)

    search_var.trace("w", lambda name, index, mode: rechercher_joueurs())

# Affectation d'une valeur à une variable
    tk.Button(buttons_frame, text="Ajouter à la comparaison", command=ajouter_joueur, bg="#0066CC", fg="white").pack(side=tk.LEFT, padx=5, pady=5)
# Affectation d'une valeur à une variable
    tk.Button(buttons_frame, text="Retirer de la comparaison", command=retirer_joueur, bg="#CC0000", fg="white").pack(side=tk.LEFT, padx=5, pady=5)
# Affectation d'une valeur à une variable
    tk.Button(buttons_frame, text="Changer type de graphe", command=switch_graph_type, bg="#FFD700", fg="black").pack(side=tk.LEFT, padx=5, pady=5)
# Affectation d'une valeur à une variable
    tk.Button(buttons_frame, text="Analyse avancée", command=analyse_selection, bg="#1E90FF", fg="white").pack(side=tk.LEFT, padx=5, pady=5)
# Affectation d'une valeur à une variable
    tk.Label(graph_frame, text="Sélectionnez des joueurs pour afficher leurs statistiques", bg="white", font=('Arial', 12)).pack(expand=True)
    rechercher_joueurs()

# Définition d'une fonction
def afficher_statistiques_par_equipe():
    #Affiche un graphique des statistiques cumulées par équipe NHL.
# Condition : si cette condition est vraie, on exécute ce bloc
    if data is None:
# Renvoie une valeur depuis une fonction
        return
# Affectation d'une valeur à une variable
    fen = tk.Toplevel(root)
    fen.title("Statistiques par Équipe")
# Affectation d'une valeur à une variable
    fen.configure(bg=COULEUR_BLEU_CIEL)
    fen.geometry("1000x700")
# Affectation d'une valeur à une variable
    frame = tk.Frame(fen, bg=COULEUR_BLEU_CIEL, padx=10, pady=10)
# Affectation d'une valeur à une variable
    frame.pack(fill=tk.BOTH, expand=True)

# Affectation d'une valeur à une variable
    tk.Label(frame, text="Statistiques des Équipes NHL", font=('Arial', 16, 'bold'), bg=COULEUR_BLEU_CIEL, fg="#0066CC").pack(pady=10)

# Affectation d'une valeur à une variable
    stats_frame = tk.Frame(frame, bg=COULEUR_BLEU_CIEL)
# Affectation d'une valeur à une variable
    stats_frame.pack(fill=tk.X, pady=10)

# Affectation d'une valeur à une variable
    tk.Label(stats_frame, text="Choisissez la statistique à afficher:", bg=COULEUR_BLEU_CIEL).pack(side=tk.LEFT, padx=5)
# Affectation d'une valeur à une variable
    stats_options = ["I_F_goals", "I_F_assists", "I_F_points"]
# Affectation d'une valeur à une variable
    stat_var = tk.StringVar(value=stats_options[0])
# Affectation d'une valeur à une variable
    stat_dropdown = ttk.Combobox(stats_frame, textvariable=stat_var, values=stats_options, state="readonly", width=15)
# Affectation d'une valeur à une variable
    stat_dropdown.pack(side=tk.LEFT, padx=5)

# Affectation d'une valeur à une variable
    graph_frame = tk.Frame(frame, bg="white")
# Affectation d'une valeur à une variable
    graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)

# Définition d'une fonction
    def mettre_a_jour_graphique():
        #Met à jour le graphique selon la statistique choisie (somme par équipe).
# Boucle for : permet de répéter une action plusieurs fois
        for widget in graph_frame.winfo_children():
            widget.destroy()
# Affectation d'une valeur à une variable
        stat_choisie = stat_var.get()
        try:
# Affectation d'une valeur à une variable
            equipe_stats = data.groupby('team')[stat_choisie].sum().sort_values(ascending=False)
# Affectation d'une valeur à une variable
            fig, ax = plt.subplots(figsize=(10, 6))
# Affectation d'une valeur à une variable
            colors = plt.cm.viridis(np.linspace(0, 0.9, len(equipe_stats)))
# Affectation d'une valeur à une variable
            bars = ax.bar(equipe_stats.index, equipe_stats.values, color=colors)
# Affectation d'une valeur à une variable
            ax.set_xlabel('Équipe', fontsize=12)
# Affectation d'une valeur à une variable
            labels_stats = {
                "I_F_goals": "Nombre total de buts",
                "I_F_assists": "Nombre total de passes décisives",
                "I_F_points": "Nombre total de points"
            }
# Affectation d'une valeur à une variable
            ax.set_ylabel(labels_stats.get(stat_choisie, stat_choisie), fontsize=12)
# Affectation d'une valeur à une variable
            plt.title(f"{labels_stats.get(stat_choisie, stat_choisie)} par équipe", fontsize=14)
# Affectation d'une valeur à une variable
            plt.xticks(rotation=45, ha='right')
# Boucle for : permet de répéter une action plusieurs fois
            for bar in bars:
# Affectation d'une valeur à une variable
                height = bar.get_height()
# Affectation d'une valeur à une variable
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{int(height)}', ha='center', va='bottom', fontsize=9)
            plt.tight_layout()
# Affectation d'une valeur à une variable
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
# Affectation d'une valeur à une variable
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except Exception as e:
# Affectation d'une valeur à une variable
            tk.Label(graph_frame, text=f"Erreur lors de la création du graphique: {str(e)}", bg="white", fg="red", font=('Arial', 10)).pack(expand=True)

# Affectation d'une valeur à une variable
    tk.Button(stats_frame, text="Afficher", command=mettre_a_jour_graphique, bg="#0066CC", fg="white").pack(side=tk.LEFT, padx=10)
    mettre_a_jour_graphique()

# Définition d'une fonction
def analyse_avancee_joueurs(joueurs, data):
    #Fenêtre d'analyse mathématique avancée pour une liste de joueurs.
# Affectation d'une valeur à une variable
    win = tk.Toplevel()
    win.title("Analyse avancée : comparaison mathématique")
    win.geometry("900x600")
# Affectation d'une valeur à une variable
    frame = tk.Frame(win, bg="#FFFFFF", padx=20, pady=20)
# Affectation d'une valeur à une variable
    frame.pack(fill=tk.BOTH, expand=True)
# Affectation d'une valeur à une variable
    result_box = scrolledtext.ScrolledText(frame, width=110, height=33, font=('Consolas', 11))
# Affectation d'une valeur à une variable
    result_box.pack(pady=5)

# Affectation d'une valeur à une variable
    cols = data.columns
# Affectation d'une valeur à une variable
    lines = []
# Boucle for : permet de répéter une action plusieurs fois
    for joueur in joueurs:
        row = data[data['display_name'] == joueur]
# Condition : si cette condition est vraie, on exécute ce bloc
        if row.empty:
            continue
# Affectation d'une valeur à une variable
        row = row.iloc[0]
# Affectation d'une valeur à une variable
        games = float(row['games_played']) if 'games_played' in row else 0
# Affectation d'une valeur à une variable
        goals = float(row['I_F_goals']) if 'I_F_goals' in row else 0
# Affectation d'une valeur à une variable
        assists = float(row['I_F_assists']) if 'I_F_assists' in row else 0
# Affectation d'une valeur à une variable
        points = float(row['I_F_points']) if 'I_F_points' in row else 0
# Affectation d'une valeur à une variable
        proj_goals = (goals / games) * 82 if games else 0
# Affectation d'une valeur à une variable
        proj_assists = (assists / games) * 82 if games else 0
# Affectation d'une valeur à une variable
        proj_points = (points / games) * 82 if games else 0
# Affectation d'une valeur à une variable
        goals_per_game = goals / games if games else 0
# Affectation d'une valeur à une variable
        assists_per_game = assists / games if games else 0
# Affectation d'une valeur à une variable
        points_per_game = points / games if games else 0
# Affectation d'une valeur à une variable
        ga_ratio = goals / assists if assists else 0
# Affectation d'une valeur à une variable
        all_pts = data['I_F_points'].astype(float)
# Affectation d'une valeur à une variable
        percentile = np.round((all_pts < points).sum() / len(all_pts) * 100, 1)
        lines.append(f"{joueur}\n"
                     f"  Buts: {goals} | Passes: {assists} | Points: {points} | Matchs: {games}\n"
                     f"  - Projection 82 matchs: {proj_goals:.1f} G / {proj_assists:.1f} A / {proj_points:.1f} PTS\n"
                     f"  - Moyenne par match: {goals_per_game:.2f} G | {assists_per_game:.2f} A | {points_per_game:.2f} PTS\n"
                     f"  - Ratio Buts/Passes: {ga_ratio:.2f}\n"
                     f"  - Classement percentile (points): top {100-percentile:.1f}%\n"
                     "-------------------------------------------------------------\n")
    result_box.insert(tk.END, "\n".join(lines))

# Définition d'une fonction
def quitter():
    #Demande confirmation avant de quitter le programme.
# Condition : si cette condition est vraie, on exécute ce bloc
    if messagebox.askyesno("Quitter", "Êtes-vous sûr de vouloir quitter l'application?"):
        root.quit()

# Définition d'une fonction
def charger_logo():
    #Charge et redimensionne le logo NHL pour l'interface principale.
    try:
# Affectation d'une valeur à une variable
        logo_path = r"nhl_logo.jpg"
# Affectation d'une valeur à une variable
        logo_image = Image.open(logo_path)
# Affectation d'une valeur à une variable
        logo_image = logo_image.resize((100, 100), Image.LANCZOS)
# Affectation d'une valeur à une variable
        logo_photo = ImageTk.PhotoImage(logo_image)
# Renvoie une valeur depuis une fonction
        return logo_photo
    except Exception as e:
# Affiche un message à l'écran
        print(f"Erreur lors du chargement du logo: {e}")
# Renvoie une valeur depuis une fonction
        return None

# Définition d'une fonction
def main():
    #Lance l'application principale Tkinter et affiche le menu principal.
    global root
# Affectation d'une valeur à une variable
    root = tk.Tk()
    root.title("Application Statistiques NHL")
# Affectation d'une valeur à une variable
    root.configure(bg=COULEUR_BLEU_CIEL)
    root.geometry("800x600")

# Affectation d'une valeur à une variable
    logo_photo = charger_logo()
# Affectation d'une valeur à une variable
    main_frame = tk.Frame(root, bg=COULEUR_BLEU_CIEL, padx=20, pady=20)
# Affectation d'une valeur à une variable
    main_frame.pack(fill=tk.BOTH, expand=True)

# Affectation d'une valeur à une variable
    header_frame = tk.Frame(main_frame, bg=COULEUR_BLEU_CIEL)
# Affectation d'une valeur à une variable
    header_frame.pack(fill=tk.X, pady=(0, 20))

# Condition : si cette condition est vraie, on exécute ce bloc
    if logo_photo:
        # Affiche le logo NHL à gauche du titre
# Affectation d'une valeur à une variable
        logo_label = tk.Label(header_frame, image=logo_photo, bg=COULEUR_BLEU_CIEL)
# Affectation d'une valeur à une variable
        logo_label.image = logo_photo
# Affectation d'une valeur à une variable
        logo_label.pack(side=tk.LEFT, padx=(0, 20))

# Affectation d'une valeur à une variable
    title_label = tk.Label(header_frame, text="Statistiques NHL", font=('Arial', 24, 'bold'), bg=COULEUR_BLEU_CIEL, fg="#0066CC")
# Affectation d'une valeur à une variable
    title_label.pack(side=tk.LEFT, fill=tk.Y)

# Affectation d'une valeur à une variable
    buttons_frame = tk.Frame(main_frame, bg=COULEUR_BLEU_CIEL)
# Affectation d'une valeur à une variable
    buttons_frame.pack(fill=tk.BOTH, expand=True)

# Affectation d'une valeur à une variable
    button_style = {
        'width': 30,
        'font': ('Arial', 12),
        'bg': "#0066CC",
        'fg': "white",
        'activebackground': "#004C99",
        'activeforeground': "white",
        'relief': tk.RAISED,
        'pady': 5
    }

    # Boutons principaux de navigation
# Affectation d'une valeur à une variable
    tk.Button(buttons_frame, text="Afficher Statistiques NHL", command=afficher_statistiques, **button_style).pack(pady=10)
# Affectation d'une valeur à une variable
    tk.Button(buttons_frame, text="Rechercher Joueur/Équipe", command=ouvrir_recherche, **button_style).pack(pady=10)
# Affectation d'une valeur à une variable
    tk.Button(buttons_frame, text="Afficher Classement", command=ouvrir_classement, **button_style).pack(pady=10)
# Affectation d'une valeur à une variable
    tk.Button(buttons_frame, text="Joueurs Aléatoires", command=afficher_joueurs_aleatoires, **button_style).pack(pady=10)
# Affectation d'une valeur à une variable
    tk.Button(buttons_frame, text="Comparaison Graphique", command=ouvrir_comparaison_graphique, **button_style).pack(pady=10)
# Affectation d'une valeur à une variable
    tk.Button(buttons_frame, text="Statistiques par Équipe", command=afficher_statistiques_par_equipe, **button_style).pack(pady=10)
# Affectation d'une valeur à une variable
    tk.Button(buttons_frame, text="Quitter", command=quitter, bg="#CC0000", fg="white", width=30, font=('Arial', 12)).pack(pady=20)
    root.mainloop()

main()