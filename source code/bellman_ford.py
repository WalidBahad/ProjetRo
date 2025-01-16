import networkx as nx
import tkinter as tk
import matplotlib.pyplot as plt
import random


def generer_graphe_oriente(n):
    G = nx.DiGraph()
    for i in range(n):
        G.add_node(f"x{i}", size=800)
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                poids = random.randint(1, 100)
                G.add_edge(f"x{i}", f"x{j}", weight=poids)
            else:
                poids = random.randint(1, 100)
                G.add_edge(f"x{j}", f"x{i}", weight=poids)
    return G


def afficher_graphe(G, chemin=None):
    pos = nx.spring_layout(G, seed=42)
    node_sizes = [G.nodes[node]['size'] for node in G]
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color="lightblue", font_weight="bold", arrows=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    if chemin:
        edges = [(chemin[i], chemin[i + 1]) for i in range(len(chemin) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=2, arrows=True)
    plt.show()


def bellman_ford_graphe(G, source, target):
    try:
        distance = nx.single_source_bellman_ford_path_length(G, source)
        chemin = nx.single_source_bellman_ford_path(G, source)[target]
        return chemin, distance[target]
    except nx.NetworkXNoPath:
        return None, None


def bellman_ford(n, start_node, end_node, parent_window):
    G = generer_graphe_oriente(n)
    chemin, distance = bellman_ford_graphe(G, start_node, end_node)

    # Create a new window to display the results
    result_window = tk.Toplevel(parent_window)
    result_window.title("Résultats Bellman-Ford")

    if chemin:
        # Display the plot in the new window
        fig, ax = plt.subplots()
        pos = nx.spring_layout(G, seed=42)
        node_sizes = [G.nodes[node]['size'] for node in G]
        nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color="lightblue", font_weight="bold", arrows=True,
                ax=ax)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
        edges = [(chemin[i], chemin[i + 1]) for i in range(len(chemin) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=2, arrows=True, ax=ax)

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=result_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Display the results
        result_text = f"Distance de {start_node} à {end_node} : {distance}\n"
        result_text += f"Chemin : {' -> '.join(chemin)}\n"
    else:
        result_text = f"Aucun chemin de {start_node} à {end_node}"

    result_label = tk.Label(result_window, text=result_text)
    result_label.pack(pady=10)
