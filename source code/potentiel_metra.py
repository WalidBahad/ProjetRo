import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


def generer_graphe_oriente(n, start_node, end_node):
    G = nx.DiGraph()
    nodes = [chr(65 + i) for i in range(n)]
    G.add_nodes_from(nodes)

    # Ensure the start node has no antecedents and the end node has no successors
    for i in range(n):
        if nodes[i] != start_node and nodes[i] != end_node:
            if random.choice([True, False]):
                G.add_edge(start_node, nodes[i], weight=random.randint(1, 10))
            if random.choice([True, False]):
                G.add_edge(nodes[i], end_node, weight=random.randint(1, 10))
            for j in range(i + 1, n):
                if nodes[j] != start_node and nodes[j] != end_node:
                    G.add_edge(nodes[i], nodes[j], weight=random.randint(1, 10))

    return G


def potentiel_metra(G, start_node, end_node):
    # Calculate the longest path using the Potentiel de Metra algorithm
    length, path = nx.single_source_dijkstra(G, start_node, end_node, weight='weight')
    return path, length


def afficher_graphe(G, path, titre="Graphe"):
    fig, ax = plt.subplots(figsize=(10, 7))
    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold',
            edge_color='gray', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{G.edges[u, v]["weight"]}' for u, v in G.edges()},
                                 ax=ax)

    # Highlight the critical path
    edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=3, edge_color='red', ax=ax)

    ax.set_title(titre)
    return fig


def execute_potentiel_metra(n, start_node, end_node, root):
    G = generer_graphe_oriente(n, start_node, end_node)
    path, length = potentiel_metra(G, start_node, end_node)

    fig = afficher_graphe(G, path, titre="Graphe Après Potentiel de Metra")

    result_window = tk.Toplevel(root)
    result_window.title("Résultats Potentiel de Metra")

    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    result_text = f"Chemin critique: {' -> '.join(path)}\n"
    result_text += f"Durée minimum: {length}"
    result_label = tk.Label(result_window, text=result_text)
    result_label.pack(pady=10)
