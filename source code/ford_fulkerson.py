import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
import random
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def generer_graphe_oriente(n, start_node, end_node):
    G = nx.DiGraph()
    nodes = [chr(65 + i) for i in range(n)]
    G.add_nodes_from(nodes)

    # Ensure the start node has no antecedents and the end node has no precedents
    for i in range(n):
        if nodes[i] != start_node and nodes[i] != end_node:
            if random.choice([True, False]):
                G.add_edge(start_node, nodes[i], capacity=random.randint(1, 10))
            if random.choice([True, False]):
                G.add_edge(nodes[i], end_node, capacity=random.randint(1, 10))
            for j in range(i + 1, n):
                if nodes[j] != start_node and nodes[j] != end_node:
                    if random.choice([True, False]):
                        G.add_edge(nodes[i], nodes[j], capacity=random.randint(1, 10))
                    else:
                        G.add_edge(nodes[j], nodes[i], capacity=random.randint(1, 10))

    return G


def afficher_graphe(G, flow_dict, titre="Graphe"):
    fig, ax = plt.subplots(figsize=(10, 7))
    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold',
            edge_color='gray', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{G.edges[u, v]["capacity"]}' for u, v in G.edges()},
                                 ax=ax)

    # Highlight the flow values on the edges
    edge_labels = {(u, v): f'{flow_dict[u][v]}/{G.edges[u, v]["capacity"]}' for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    ax.set_title(titre)
    return fig


def ford_fulkerson(n, start_node, end_node, root):
    start_time = time.time()

    G = generer_graphe_oriente(n, start_node, end_node)

    flow_value, flow_dict = nx.maximum_flow(G, start_node, end_node, capacity='capacity')

    fig = afficher_graphe(G, flow_dict, titre="Graphe Après Ford-Fulkerson")

    result_window = tk.Toplevel(root)
    result_window.title("Résultats Ford-Fulkerson")

    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    result_text = f"Valeur du flux maximum: {flow_value}\n"

    end_time = time.time()
    execution_time = end_time - start_time
    result_text += f"Temps d'exécution: {execution_time:.4f} secondes"

    result_label = tk.Label(result_window, text=result_text)
    result_label.pack(pady=10)

    # Display iterations
    iterations_text = "Iterations:\n"
    for u in flow_dict:
        for v in flow_dict[u]:
            if flow_dict[u][v] > 0:
                iterations_text += f"{u} -> {v}: {flow_dict[u][v]}/{G.edges[u, v]['capacity']}\n"

    iterations_label = tk.Label(result_window, text=iterations_text)
    iterations_label.pack(pady=10)
