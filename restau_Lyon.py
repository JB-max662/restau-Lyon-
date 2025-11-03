import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# Charger les données depuis le fichier Excel
try:
    df = pd.read_excel("restaurants_complet.xlsx")
    restaurants = df.to_dict(orient="records")
except FileNotFoundError:
    messagebox.showerror("Erreur", "Le fichier 'restaurants_complet.xlsx' est introuvable !")
    restaurants = []

# Fonction pour filtrer les restaurants
def filtrer_restaurants(note_min, prix_selectionne, types_selectionnes):
    resultats = []
    for resto in restaurants:
        if resto['note'] >= note_min:
            if prix_selectionne == "Tous" or resto['prix'] == prix_selectionne:
                if not types_selectionnes or resto['type'] in types_selectionnes:
                    resultats.append(resto)
    return resultats

# Fonction pour afficher les résultats
def afficher_resultats(resultats):
    result_window = tk.Toplevel(root)
    result_window.title("Restaurants trouvés")
    result_window.geometry("500x400")

    ttk.Label(result_window, text="Restaurants correspondants", font=("Arial", 14, "bold")).pack(pady=10)

    if resultats:
        for resto in resultats:
            text = f"{resto['nom']} - Note: {resto['note']} - Prix: {resto['prix']} - Type: {resto['type']}"
            ttk.Label(result_window, text=text, wraplength=480, justify="left").pack(anchor="w", padx=10, pady=3)
    else:
        ttk.Label(result_window, text="Aucun restaurant ne correspond aux critères.", foreground="red").pack(pady=20)

# Fonction pour filtrer par critères
def chercher_restaurants():
    note_min = note_var.get()
    prix_selectionne = prix_var.get()
    types_selectionnes = [type_ for type_, var in type_vars.items() if var.get() == 1]

    resultats = filtrer_restaurants(note_min, prix_selectionne, types_selectionnes)
    afficher_resultats(resultats)

# Fonction pour rechercher par nom via menu déroulant
def chercher_par_nom():
    nom_selectionne = nom_var.get()
    if nom_selectionne == "Tous les restaurants":
        resultats = restaurants
    else:
        resultats = [resto for resto in restaurants if resto['nom'] == nom_selectionne]

    afficher_resultats(resultats)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Filtrer les restaurants à Lyon")
root.geometry("600x750")
root.configure(bg="#f2f2f2")

# Titre
ttk.Label(root, text="Filtre de Restaurants à Lyon", font=("Arial", 18, "bold")).pack(pady=20)

# Note minimale
ttk.Label(root, text="Note minimale (sur 5) :").pack()
note_var = tk.DoubleVar(value=0)
note_slider = ttk.Scale(root, from_=0, to=5, orient="horizontal", variable=note_var)
note_slider.pack(pady=10)

# Prix
ttk.Label(root, text="Prix :").pack()
prix_var = tk.StringVar(value="Tous")
prix_options = ["Tous", "€", "€€", "€€€"]
prix_menu = ttk.OptionMenu(root, prix_var, prix_var.get(), *prix_options)
prix_menu.pack(pady=10)

# Type de nourriture
ttk.Label(root, text="Type de nourriture :").pack()
type_frame = ttk.Frame(root)
type_frame.pack(pady=5)
type_vars = {}
types = sorted(set(resto['type'] for resto in restaurants))
for t in types:
    var = tk.IntVar()
    cb = ttk.Checkbutton(type_frame, text=t, variable=var)
    cb.pack(anchor="w")
    type_vars[t] = var

# Bouton pour filtrer par critères
ttk.Button(root, text="Filtrer par critères", command=chercher_restaurants).pack(pady=20)

# Menu déroulant pour sélectionner un restaurant
ttk.Label(root, text="Sélectionner un restaurant :").pack(pady=5)
nom_var = tk.StringVar(value="Tous les restaurants")
noms_restaurants = ["Tous les restaurants"] + [resto['nom'] for resto in restaurants]
nom_menu = ttk.OptionMenu(root, nom_var, nom_var.get(), *noms_restaurants)
nom_menu.pack(pady=5)
ttk.Button(root, text="Chercher par nom", command=chercher_par_nom).pack(pady=10)
#
# Lancer l'application
root.mainloop()

