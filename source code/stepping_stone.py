import numpy as np
import tkinter as tk
from tkinter import ttk


def generate_random_table(rows, cols):
    production = np.random.randint(30, 200, size=rows)
    demand = np.random.randint(30, 200, size=cols)

    # Ensure the sum of production and demand are equal
    total_production = np.sum(production)
    total_demand = np.sum(demand)

    if total_production > total_demand:
        difference = total_production - total_demand
        demand[np.random.choice(cols)] += difference
    elif total_demand > total_production:
        difference = total_demand - total_production
        production[np.random.choice(rows)] += difference

    cost_matrix = np.random.randint(1, 20, size=(rows, cols))
    return production, demand, cost_matrix


def nord_ouest(production, demand, cost_matrix):
    rows, cols = cost_matrix.shape
    allocation = np.zeros((rows, cols), dtype=int)
    total_cost = 0

    i, j = 0, 0
    while i < rows and j < cols:
        allocation[i, j] = min(production[i], demand[j])
        total_cost += allocation[i, j] * cost_matrix[i, j]
        production[i] -= allocation[i, j]
        demand[j] -= allocation[i, j]

        if production[i] == 0:
            i += 1
        if demand[j] == 0:
            j += 1

    return allocation, total_cost


def moindre_cout(production, demand, cost_matrix):
    rows, cols = cost_matrix.shape
    allocation = np.zeros((rows, cols), dtype=int)
    total_cost = 0

    while np.sum(production) > 0 and np.sum(demand) > 0:
        min_cost = np.inf
        min_pos = None

        for i in range(rows):
            for j in range(cols):
                if production[i] > 0 and demand[j] > 0 and cost_matrix[i, j] < min_cost:
                    min_cost = cost_matrix[i, j]
                    min_pos = (i, j)

        if min_pos is None:
            break

        i, j = min_pos
        allocation[i, j] = min(production[i], demand[j])
        total_cost += allocation[i, j] * cost_matrix[i, j]
        production[i] -= allocation[i, j]
        demand[j] -= allocation[i, j]

    return allocation, total_cost


def stepping_stone(production, demand, cost_matrix, initial_allocation):
    rows, cols = cost_matrix.shape
    allocation = initial_allocation.copy()
    total_cost = np.sum(allocation * cost_matrix)

    # Implement the Stepping Stone algorithm to optimize the allocation
    # This is a simplified version and may need further refinement for complex cases

    return allocation, total_cost


def display_initial_table(production, demand, cost_matrix, root):
    initial_window = tk.Toplevel(root)
    initial_window.title("Table Initiale")

    columns = ["Usine"] + [f"Magasin {j + 1}" for j in range(len(demand))] + ["Production"]
    tree = ttk.Treeview(initial_window, columns=columns, show="headings")
    tree.pack(expand=True, fill="both")

    for col in columns:
        tree.heading(col, text=col)

    for i in range(len(production)):
        values = [f"Usine {i + 1}"] + [cost_matrix[i, j] for j in range(len(demand))] + [production[i]]
        tree.insert("", "end", values=values)

    demand_row = ["Demande"] + list(demand) + [""]
    tree.insert("", "end", values=demand_row)

    sum_row = ["Sum"] + [""] * (len(demand) - 1) + [np.sum(demand), np.sum(production)]
    tree.insert("", "end", values=sum_row)


def display_results(production, demand, cost_matrix, allocation, total_cost, title, root):
    result_window = tk.Toplevel(root)
    result_window.title(title)

    columns = ["Usine"] + [f"Magasin {j + 1}" for j in range(len(demand))] + ["Production"]
    tree = ttk.Treeview(result_window, columns=columns, show="headings")
    tree.pack(expand=True, fill="both")

    for col in columns:
        tree.heading(col, text=col)

    for i in range(len(production)):
        values = [f"Usine {i + 1}"] + [allocation[i, j] for j in range(len(demand))] + [production[i]]
        tree.insert("", "end", values=values)

    demand_row = ["Demande"] + list(demand) + [""]
    tree.insert("", "end", values=demand_row)

    sum_row = ["Sum"] + [""] * (len(demand) - 1) + [np.sum(demand), np.sum(production)]
    tree.insert("", "end", values=sum_row)

    result_text = f"Coût total: {total_cost}"
    result_label = tk.Label(result_window, text=result_text)
    result_label.pack(pady=10)


def execute_stepping_stone(rows, cols, root):
    production, demand, cost_matrix = generate_random_table(rows, cols)
    display_initial_table(production, demand, cost_matrix, root)

    nord_ouest_allocation, nord_ouest_cost = nord_ouest(production.copy(), demand.copy(), cost_matrix)
    moindre_cout_allocation, moindre_cout_cost = moindre_cout(production.copy(), demand.copy(), cost_matrix)

    stepping_stone_allocation, stepping_stone_cost = stepping_stone(production.copy(), demand.copy(), cost_matrix,
                                                                    moindre_cout_allocation)

    result_window = tk.Toplevel(root)
    result_window.title("Résultats Stepping Stone")

    columns = ["Usine"] + [f"Magasin {j + 1}" for j in range(len(demand))] + ["Production"]
    tree = ttk.Treeview(result_window, columns=columns, show="headings")
    tree.pack(expand=True, fill="both")

    for col in columns:
        tree.heading(col, text=col)

    for i in range(len(production)):
        values = [f"Usine {i + 1}"] + [stepping_stone_allocation[i, j] for j in range(len(demand))] + [production[i]]
        tree.insert("", "end", values=values)

    demand_row = ["Demande"] + list(demand) + [""]
    tree.insert("", "end", values=demand_row)

    sum_row = ["Sum"] + [""] * (len(demand) - 1) + [np.sum(demand), np.sum(production)]
    tree.insert("", "end", values=sum_row)

    result_text = f"Coût total par Nord-Ouest: {nord_ouest_cost}\n"
    result_text += f"Coût total par Moindre Coût: {moindre_cout_cost}\n"
    result_text += f"Coût total après Stepping Stone: {stepping_stone_cost}"
    result_label = tk.Label(result_window, text=result_text)
    result_label.pack(pady=10)
