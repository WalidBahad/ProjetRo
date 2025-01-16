import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generer_graphe_aleatoire(n, p):
    orienté = random.choice([True, False])
    if orienté:
        G = nx.gnp_random_graph(n, p, directed=True)
    else:
        G = nx.gnp_random_graph(n, p, directed=False)
    return G, orienté

def coloration_welsh_powell(G):
    # Apply Welsh-Powell algorithm for coloring
    colors = nx.coloring.greedy_color(G, strategy="largest_first")
    return colors

def afficher_graphe(G, couleurs_noeuds=None, titre="Graphe"):
    fig, ax = plt.subplots(figsize=(10, 7))
    pos = nx.spring_layout(G)

    if couleurs_noeuds is not None:
        nx.draw(G, pos, node_color=[couleurs_noeuds[n] for n in G.nodes()], with_labels=True, node_size=500,
                cmap=plt.cm.rainbow, ax=ax)
    else:
        nx.draw(G, pos, node_color='blue', with_labels=True, node_size=500, ax=ax)

    ax.set_title(titre)
    return fig

def execute_welsh_powel(n, root):
    # Mesure du temps d'exécution total
    start_time = time.time()

    # La probabilité qu'un sommet soit lié à un autre
    p = 0.7

    G, orienté = generer_graphe_aleatoire(n, p)

    # Coloration après Welsh-Powell
    couleurs_noeuds_après = coloration_welsh_powell(G)
    min_couleur_après = max(couleurs_noeuds_après.values()) + 1  # Number of colors used after Welsh-Powell

    # Afficher le graphe avec la coloration après Welsh-Powell
    fig = afficher_graphe(G, couleurs_noeuds=couleurs_noeuds_après, titre="Graphe Après Welsh-Powell")

    # Create a new window to display the results
    result_window = tk.Toplevel(root)
    result_window.title("Résultats Welsh-Powell")

    # Display the plot in the new window
    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Display the results
    result_text = f"Nombre minimum de couleurs (après Welsh-Powell): {min_couleur_après}\n"
    result_text += f"Formule selon Welsh-Powell: {min_couleur_après} <= Xi(G) <= {n}\n"

    # Afficher le temps d'exécution total
    end_time = time.time()
    execution_time = end_time - start_time
    result_text += f"Temps d'exécution total: {execution_time:.4f} secondes"

    result_label = tk.Label(result_window, text=result_text)
    result_label.pack(pady=10)
