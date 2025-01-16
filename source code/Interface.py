import tkinter as tk
from tkinter import PhotoImage
from welsh_powel import execute_welsh_powel
from kruskal import execute_kruskal
from dijkstra import dijkstra
from bellman_ford import bellman_ford
from moindre_cout import execute_moindre_cout
from nord_ouest import execute_nord_ouest
from stepping_stone import execute_stepping_stone
from ford_fulkerson import ford_fulkerson
from potentiel_metra import execute_potentiel_metra
from PIL import Image, ImageTk
import base64
from io import BytesIO
from embedded_image import image_data
import sys,os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Function to center a window
def center_window(window, width=400, height=300):
    window.geometry(f"{width}x{height}")
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Function to add hover effects
def add_hover_effects(button):
    def on_enter(event):
        button.config(bg="#4CAF50", fg="white")

    def on_leave(event):
        button.config(bg="#2F4F4F", fg="white")

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# New function to open the "About Me" window
def open_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("About Me")
    center_window(about_window, width=800, height=700)

    # Frame pour organiser le contenu
    frame = tk.Frame(about_window, bg="#E8E8E8")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Charger et afficher l'image
    img_path = resource_path("logo-1.png")  # Assurez-vous que le fichier est au bon endroit
    try:
        img = Image.open(img_path)
        img = img.resize((550, 300))  # Ajustez la taille de l'image
        photo = ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Erreur de chargement de l'image : {e}")
        photo = None

    if photo:
        label_image = tk.Label(frame, image=photo, bg="#E8E8E8")
        label_image.image = photo  # Référence pour éviter le garbage collection
        label_image.pack(pady=10)

    # Texte de présentation
    intro_text = (
        "This project was realised by the student: WALID BAHAD\n\n"
        "Under the guidance of professor: EL MKHALET MOUNA\n\n"
        "CM: RECHERCHE OPERATIONNELLE - 2025\n\n"
    )
    intro_label = tk.Label(frame, text=intro_text, font=("Arial", 12), bg="#E8E8E8", fg="black", justify="center")
    intro_label.pack(pady=20)

    # Bouton pour fermer la fenêtre
    close_button = tk.Button(about_window, text="Close", command=about_window.destroy, bg="#DC143C", fg="white")
    close_button.pack(pady=10, fill="x")
    add_hover_effects(close_button)

def open_algorithm_window():
    algorithm_window = tk.Toplevel(root)
    algorithm_window.title("Select Algorithm")
    center_window(algorithm_window, width=500, height=400)

    # Frame for buttons
    frame = tk.Frame(algorithm_window, bg="#E8E8E8")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    def execute_algorithm(algorithm_name):
        input_window = tk.Toplevel(algorithm_window)
        input_window.title(f"Input for {algorithm_name}")
        center_window(input_window, width=400, height=350)

        def on_submit():
            if algorithm_name == "Welsh Powel":
                n = int(entry_n.get())
                execute_welsh_powel(n, result_label)
            elif algorithm_name == "Kruskal":
                n = int(entry_n.get())
                execute_kruskal(n, result_label)
            elif algorithm_name == "Dijkstra":
                n = int(entry_n.get())
                start_node = entry_start.get()
                dijkstra(n, start_node, result_label)
            elif algorithm_name == "Bellman-Ford":
                n = int(entry_n.get())
                start_node = entry_start.get()
                end_node = entry_end.get()
                bellman_ford(n, start_node, end_node, result_label)
            elif algorithm_name == "Moindre Cout":
                rows = int(entry_n.get())
                cols = int(entry_m.get())
                execute_moindre_cout(rows, cols, result_label)
            elif algorithm_name == "Nord Ouest":
                rows = int(entry_n.get())
                cols = int(entry_m.get())
                execute_nord_ouest(rows, cols, result_label)
            elif algorithm_name == "Stepping Stone":
                rows = int(entry_n.get())
                cols = int(entry_m.get())
                execute_stepping_stone(rows, cols, result_label)
            elif algorithm_name == "Ford Fulkerson":
                n = int(entry_n.get())
                start_node = entry_start.get()
                end_node = entry_end.get()
                ford_fulkerson(n, start_node, end_node, result_label)
            elif algorithm_name == "Potentiel de Metra":
                n = int(entry_n.get())
                start_node = entry_start.get()
                end_node = entry_end.get()
                execute_potentiel_metra(n, start_node, end_node, result_label)
            input_window.destroy()

        # Create dynamic input fields based on the algorithm
        label = tk.Label(input_window, text=f"Inputs for {algorithm_name}", font=("Arial", 12, "bold"))
        label.pack(pady=10)

        if algorithm_name in ["Welsh Powel", "Kruskal"]:
            label_n = tk.Label(input_window, text="Entrer le nombre de sommets:")
            label_n.pack(pady=5)
            entry_n = tk.Entry(input_window)
            entry_n.pack(pady=5)
        elif algorithm_name in ["Dijkstra"]:
            label_n = tk.Label(input_window, text="Entrer le nombre de sommets :")
            label_n.pack(pady=5)
            entry_n = tk.Entry(input_window)
            entry_n.pack(pady=5)
            label_start = tk.Label(input_window, text="Entrez le sommet de départX{1..}:")
            label_start.pack(pady=5)
            entry_start = tk.Entry(input_window)
            entry_start.pack(pady=5)
        elif algorithm_name in ["Bellman-Ford", "Ford Fulkerson"]:
            label_n = tk.Label(input_window, text="Entrez le nombre de sommets:")
            label_n.pack(pady=10)
            entry_n = tk.Entry(input_window)
            entry_n.pack(pady=10)
            label_start = tk.Label(input_window, text="Entrez le sommet de départ x{1..n}:")
            label_start.pack(pady=10)
            entry_start = tk.Entry(input_window)
            entry_start.pack(pady=10)
            label_end = tk.Label(input_window, text="Entrez le sommet d'arrivée x{1..n}:")
            label_end.pack(pady=10)
            entry_end = tk.Entry(input_window)
            entry_end.pack(pady=10)
        elif algorithm_name in ["Moindre Cout", "Nord Ouest", "Stepping Stone"]:
            label_n = tk.Label(input_window, text="Entrez le nombre de lignes:")
            label_n.pack(pady=10)
            entry_n = tk.Entry(input_window)
            entry_n.pack(pady=10)
            label_m = tk.Label(input_window, text="Entrez le nombre de colonnes:")
            label_m.pack(pady=10)
            entry_m = tk.Entry(input_window)
            entry_m.pack(pady=10)
        elif algorithm_name == "Potentiel de Metra":
            label_n = tk.Label(input_window, text="Entrez le nombre de sommets:")
            label_n.pack(pady=10)
            entry_n = tk.Entry(input_window)
            entry_n.pack(pady=10)
            label_start = tk.Label(input_window, text="Entrez le sommet de départ (A-Z):")
            label_start.pack(pady=10)
            entry_start = tk.Entry(input_window)
            entry_start.pack(pady=10)
            label_end = tk.Label(input_window, text="Entrez le sommet d'arrivée (A-Z):")
            label_end.pack(pady=10)
            entry_end = tk.Entry(input_window)
            entry_end.pack(pady=10)


        submit_button = tk.Button(input_window, text="Submit", command=on_submit, bg="#2F4F4F", fg="white")
        submit_button.pack(pady=10)
        add_hover_effects(submit_button)

    algorithms = [
        "Welsh Powel",
        "Kruskal",
        "Dijkstra",
        "Bellman-Ford",
        "Moindre Cout",
        "Nord Ouest",
        "Stepping Stone",
        "Ford Fulkerson",
        "Potentiel de Metra",
    ]
    for algorithm in algorithms:
        button = tk.Button(frame, text=algorithm, command=lambda alg=algorithm: execute_algorithm(alg),
                           bg="#2F4F4F", fg="white", font=("Arial", 10, "bold"))
        button.pack(pady=5, fill="x")
        add_hover_effects(button)

    close_button = tk.Button(algorithm_window, text="Close", command=algorithm_window.destroy,
                             bg="#DC143C", fg="white", font=("Arial", 10, "bold"))
    close_button.pack(pady=10, fill="x")
    add_hover_effects(close_button)

def quit_application():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Algorithm Executor")

root.configure(bg="#F0F0F0")
root.geometry("500x400")

# Create buttons
entry_button = tk.Button(root, text="Entrer", command=open_algorithm_window, bg="#2F4F4F", fg="white", font=("Arial", 12, "bold"))
entry_button.pack(pady=10, fill="x")
add_hover_effects(entry_button)

# About Me button
about_button = tk.Button(root, text="About Me", command=open_about_window, bg="#2F4F4F", fg="white", font=("Arial", 12, "bold"))
about_button.pack(pady=10, fill="x")
add_hover_effects(about_button)


sortie_button = tk.Button(root, text="Sortie", command=quit_application, bg="#DC143C", fg="white", font=("Arial", 12, "bold"))
sortie_button.pack(pady=10, fill="x")
add_hover_effects(sortie_button)




result_label = tk.Label(root, text="", font=("Arial", 10), bg="#F0F0F0", fg="black")
result_label.pack(pady=10)

center_window(root)
root.mainloop()
