import string
import random
import time
import tkinter as tk
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fonction pour générer les étiquettes des nœuds (A, B, ..., Z, AA, AB, ..., ZZ)
def generer_etiquettes_sommets(nb_sommets):
    alphabet = string.ascii_uppercase
    etiquettes = []
    for i in range(nb_sommets):
        etiquette = ""
        while i >= 0:
            etiquette = alphabet[i % 26] + etiquette
            i = i // 26 - 1
        etiquettes.append(etiquette)
    return etiquettes

# Fonction pour générer un graphe non orienté avec des poids aléatoires
def generer_graphe(nb_sommets):
    sommets = generer_etiquettes_sommets(nb_sommets)
    aretes = []
    for i in range(nb_sommets):
        for j in range(i + 1, nb_sommets):
            poids = random.randint(1, 1000)  # Poids aléatoires entre 1 et 1000
            aretes.append((sommets[i], sommets[j], poids))
    return sommets, aretes

# Classe de l'ensemble disjoint (Union-Find) pour détecter les cycles
class EnsembleDisjoint:
    def __init__(self, nb_sommets):
        self.parent = list(range(nb_sommets))
        self.rang = [0] * nb_sommets

    # Trouver le représentant (racine) de l'ensemble du sommet u
    def trouver(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.trouver(self.parent[u])
        return self.parent[u]

    # Union des ensembles des sommets u et v
    def union(self, u, v):
        racine_u = self.trouver(u)
        racine_v = self.trouver(v)
        if racine_u != racine_v:
            if self.rang[racine_u] > self.rang[racine_v]:
                self.parent[racine_v] = racine_u
            elif self.rang[racine_u] < self.rang[racine_v]:
                self.parent[u] = racine_v
            else:
                self.parent[racine_v] = racine_u
                self.rang[racine_u] += 1

# Algorithme de Kruskal pour trouver l'Arbre Couvrant Minimum (ACM)
def kruskal(sommets, aretes):
    # Trier les arêtes par poids
    aretes_triees = sorted(aretes, key=lambda x: x[2])
    ensemble_disjoint = EnsembleDisjoint(len(sommets))

    arbre_couvrant_min = []  # Liste pour l'Arbre Couvrant Minimum (ACM)
    cout_total = 0  # Coût total de l'ACM

    # Parcourir les arêtes triées
    for arete in aretes_triees:
        sommet_u, sommet_v, poids = arete
        indice_u = sommets.index(sommet_u)
        indice_v = sommets.index(sommet_v)

        # Vérifier si l'ajout de cette arête crée un cycle
        if ensemble_disjoint.trouver(indice_u) != ensemble_disjoint.trouver(indice_v):
            ensemble_disjoint.union(indice_u, indice_v)
            arbre_couvrant_min.append(arete)
            cout_total += poids

            # Arrêter quand on a n-1 arêtes dans l'ACM
            if len(arbre_couvrant_min) == len(sommets) - 1:
                break

    return arbre_couvrant_min, cout_total

# Fonction pour visualiser le graphe avec NetworkX
def visualiser_graphe(sommets, aretes, acm=None, titre="Graphe"):
    G = nx.Graph()

    # Ajouter les arêtes au graphe
    for sommet_u, sommet_v, poids in aretes:
        G.add_edge(sommet_u, sommet_v, weight=poids)

    # Positionner les nœuds dans l'espace
    pos = nx.spring_layout(G, seed=42)  # Positionnement fixe pour cohérence

    # Dessiner le graphe complet
    fig, ax = plt.subplots(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold',
            edge_color='gray', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{poids}' for u, v, poids in aretes}, ax=ax)

    # Surligner l'Arbre Couvrant Minimum si fourni
    if acm:
        aretes_acm = [(sommet_u, sommet_v) for sommet_u, sommet_v, _ in acm]
        nx.draw_networkx_edges(G, pos, edgelist=aretes_acm, width=3, edge_color='blue', ax=ax)

    ax.set_title(titre)
    return fig

def execute_kruskal(nb_sommets, root):
    debut_temps = time.time()  # Démarrer le chronomètre

    # Générer le graphe
    sommets, aretes = generer_graphe(nb_sommets)

    # Appliquer l'algorithme de Kruskal
    acm, cout_total = kruskal(sommets, aretes)

    # Visualiser l'ACM après Kruskal
    fig = visualiser_graphe(sommets, aretes, acm, titre="Graphe Après Kruskal (ACM)")

    # Create a new window to display the results
    result_window = tk.Toplevel(root)
    result_window.title("Résultats Kruskal")

    # Display the plot in the new window
    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Display the results
    result_text = f"Coût Total de l'Arbre Couvrant Minimum: {cout_total} euro\n"

    # Afficher le temps d'exécution total
    fin_temps = time.time()
    execution_time = fin_temps - debut_temps
    result_text += f"Temps d'exécution: {execution_time:.4f} secondes"

    result_label = tk.Label(result_window, text=result_text)
    result_label.pack(pady=10)
