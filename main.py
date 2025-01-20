import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import shutil
import ctypes
import os
import json

def check_admin():
    """Sprawdza, czy program działa jako administrator."""
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False
    return is_admin

def restart_as_admin():
    """Ponownie uruchamia aplikację jako administrator."""
    if not check_admin():
        # Przygotowanie argumentów do uruchomienia jako administrator
        script = sys.executable
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 0)
        sys.exit()  # Zamknięcie aktualnej instancji

# Wymuszenie uruchomienia jako administrator
restart_as_admin()

def cleanup_temp():
    if hasattr(sys, '_MEIPASS'):
        temp_dir = sys._MEIPASS
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Nie udało się usunąć katalogu tymczasowego: {e}")

import atexit
atexit.register(cleanup_temp)

# Funkcja uruchamiania komend
def run_command(command):
    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się uruchomić komendy: {e}")

def change_language(lang):
    if lang == "EN":
        messagebox.showinfo("Language Change", "Language changed to English.")
        restart_with_language("EN")
    elif lang == "PL":
        messagebox.showinfo("Language Change", "Język zmieniony na polski.")
        restart_with_language("PL")

def restart_with_language(lang):
    """Ponownie uruchamia aplikację z wybranym językiem."""
    script = sys.executable
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    params += f' --lang={lang}'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 0)
    sys.exit()

def get_resource_path(filename):
    """Zwraca pełną ścieżkę do zasobu w katalogu projektu."""
    if getattr(sys, 'frozen', False):  # Sprawdzenie, czy aplikacja jest skompilowana
        base_path = sys._MEIPASS  # Folder tymczasowy stworzony przez PyInstaller
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Ścieżka do skryptu
    return os.path.join(base_path, filename)

def load_commands(lang):
    # Wybór pliku JSON
    if lang == "EN":
        filepath = get_resource_path("commandsEN.json")
    else:
        filepath = get_resource_path("commandsPL.json")
    
    # Wczytanie danych z pliku
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def main():
    # Sprawdzenie argumentów wiersza poleceń dla języka
    lang = "PL"  # Domyślny język
    for arg in sys.argv:
        if arg.startswith("--lang="):
            lang = arg.split("=")[1]

    # Załaduj komendy z pliku
    data = load_commands(lang)

    # Tworzenie okna aplikacji
    root = tk.Tk()
    root.title("Command Runner")
    root.geometry("900x500")
    root.configure(bg="#2C3E50")
    root.iconbitmap(get_resource_path("icon.ico"))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#34495E",
                    foreground="white",
                    rowheight=25,
                    fieldbackground="#34495E",
                    font=("Arial", 10))
    style.map("Treeview", background=[("selected", "#1ABC9C")])

    # Funkcja do odświeżania tabeli
    def refresh_table(filter_text=""):
        for row in tree.get_children():
            tree.delete(row)

        filtered_data = [row for row in data if filter_text.lower() in row["Command"].lower() or filter_text.lower() in row["Description"].lower()]

        for row in filtered_data:
            tree.insert("", "end", values=(row["ID"], row["Command"], row["Description"]))

    # Tworzenie pola wyszukiwania
    search_frame = tk.Frame(root, bg="#2C3E50")
    search_frame.pack(fill="x", padx=10, pady=10)

    search_label = tk.Label(search_frame, text="Szukaj:" if lang == "PL" else "Search:", bg="#2C3E50", fg="white", font=("Arial", 12))
    search_label.pack(side="left", padx=5)

    search_entry = tk.Entry(search_frame, font=("Arial", 12))
    search_entry.pack(side="left", fill="x", expand=True, padx=5)

    # Bind dynamicznego wyszukiwania
    def on_search(event):
        refresh_table(search_entry.get())

    search_entry.bind("<KeyRelease>", on_search)

    # Tworzenie tabeli z paskiem przewijania
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(tree_frame, columns=("ID", "Command", "Description"), show="headings", selectmode="browse", yscrollcommand=tree_scroll.set)
    tree.heading("ID", text="ID")
    tree.heading("Command", text="Command")
    tree.heading("Description", text="Description")
    tree.column("ID", width=50, anchor="w")
    tree.column("Command", width=200, anchor="w")
    tree.column("Description", width=500, anchor="w")
    tree.pack(fill="both", expand=True)

    tree_scroll.config(command=tree.yview)

    # Funkcja do obsługi podwójnego kliknięcia
    def on_double_click(event):
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Uwaga" if lang == "PL" else "Warning", "Wybierz komendę do uruchomienia." if lang == "PL" else "Select a command to run.")
            return

        command = tree.item(selected_item, "values")[1]
        run_command(command)

    tree.bind("<Double-1>", on_double_click)

    # Funkcja do obsługi przycisku RUN
    def on_run():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Uwaga" if lang == "PL" else "Warning", "Wybierz komendę do uruchomienia." if lang == "PL" else "Select a command to run.")
            return

        command = tree.item(selected_item, "values")[1]
        run_command(command)

    # Przyciski
    button_frame = tk.Frame(root, bg="#2C3E50")
    button_frame.pack(pady=10)

    run_button = tk.Button(button_frame, text="RUN", command=on_run, bg="#1ABC9C", fg="white", font=("Arial", 12), padx=20)
    run_button.pack(side="left", padx=5)

    quit_button = tk.Button(button_frame, text="EXIT" if lang == "EN" else "WYJŚCIE", command=root.destroy, bg="#E74C3C", fg="white", font=("Arial", 12), padx=20)
    quit_button.pack(side="left", padx=5)

    # Przycisk zmiany języka
    lang_button_frame = tk.Frame(root, bg="#2C3E50")
    lang_button_frame.pack(pady=10)

    lang_en_button = tk.Button(lang_button_frame, text="EN", command=lambda: change_language("EN"), bg="#3498DB", fg="white", font=("Arial", 12), padx=20)
    lang_en_button.pack(side="left", padx=5)

    lang_pl_button = tk.Button(lang_button_frame, text="PL", command=lambda: change_language("PL"), bg="#3498DB", fg="white", font=("Arial", 12), padx=20)
    lang_pl_button.pack(side="left", padx=5)

    lang_button_frame.pack(side="right", padx=10)

    # Dodanie napisu w lewym dolnym rogu
    footer_label = tk.Label(root, text="Kuzyn Entertaiment Production", bg="#2C3E50", fg="#E74C3C", font=("Arial", 10, "bold"))
    footer_label.pack(side="left", anchor="sw", padx=10, pady=10)

    # Odświeżenie tabeli na start
    refresh_table()

    # Uruchomienie pętli głównej aplikacji
    root.mainloop()

if __name__ == "__main__":
    # Sprawdzenie argumentów wiersza poleceń dla języka
    lang = "PL"  # Domyślny język
    for arg in sys.argv:
        if arg.startswith("--lang="):
            lang = arg.split("=")[1]

    main()
