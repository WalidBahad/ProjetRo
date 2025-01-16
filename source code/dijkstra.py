import matplotlib.pyplot as plt
import networkx as nx
import random
import tkinter as tk
import heapq

def dijkstra(num_nodes, start_node, parent_window):
    # Generate the graph
    graph = generate_graph(num_nodes)

    # Validate starting node
    if start_node not in graph.nodes():
        error_window = tk.Toplevel(parent_window)
        error_window.title("Error")
        tk.Label(error_window, text=f"Error: {start_node} is not a valid node.").pack(pady=10)
        tk.Button(error_window, text="Close", command=error_window.destroy).pack(pady=10)
        return

    # Initialize data structures
    priority_queue = [(0, start_node)]  # (distance, node)
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start_node] = 0
    paths = {node: [] for node in graph.nodes()}
    paths[start_node] = [start_node]
    visited = set()

    # Perform Dijkstra's algorithm
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if already visited
        if current_node in visited:
            continue

        # Mark the node as visited
        visited.add(current_node)

        # Check all neighbors of the current node
        for neighbor in graph.neighbors(current_node):
            edge_weight = graph[current_node][neighbor]['weight']
            new_distance = current_distance + edge_weight

            # Update distances and path if a shorter path is found
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                paths[neighbor] = paths[current_node] + [neighbor]
                heapq.heappush(priority_queue, (new_distance, neighbor))

    # Display results in a new GUI window
    result_window = tk.Toplevel(parent_window)
    result_window.title("Dijkstra's Algorithm Results")

    # Create a text widget to display paths and distances
    result_text = tk.Text(result_window, wrap="word", width=50, height=20)
    result_text.pack(pady=10)
    result_text.insert("end", "Shortest Paths:\n\n")

    for dest, distance in distances.items():
        path_str = " -> ".join(paths[dest])
        result_text.insert("end", f"{dest}: {distance} ({path_str})\n")

    # Add a button to show the graph
    def show_graph():
        plot_graph(graph, paths, start_node, "Graph with Shortest Paths Highlighted")

    tk.Button(result_window, text="Show Graph", command=show_graph).pack(pady=10)

    # Add a close button
    tk.Button(result_window, text="Close", command=result_window.destroy).pack(pady=10)


# Function to generate a random graph
def generate_graph(num_nodes, max_weight=100):
    graph = nx.Graph()
    nodes = [f"X{i + 1}" for i in range(num_nodes)]
    graph.add_nodes_from(nodes)

    # Randomly add edges with weights between nodes
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = random.randint(1, max_weight)
            graph.add_edge(nodes[i], nodes[j], weight=weight)

    return graph


# Function to plot the graph
def plot_graph(graph, paths, start_node, title):
    pos = nx.spring_layout(graph, seed=42)

    # Highlight edges in the shortest paths
    edges_in_paths = [(u, v) for path in paths.values() for u, v in zip(path, path[1:])]
    edge_colors = ['red' if (u, v) in edges_in_paths or (v, u) in edges_in_paths else 'black' for u, v in graph.edges()]
    node_colors = ['lightgreen' if n == start_node else 'lightgrey' for n in graph.nodes()]

    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=500, font_size=10)
    nx.draw_networkx_edge_labels(graph, pos,
                                 edge_labels={(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)})

    plt.title(title)
    plt.show()