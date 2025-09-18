# mini_dnevnik_gui.py

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv
import os
from collections import Counter
import matplotlib.pyplot as plt

FAJL = r"C:\Users\mirko\OneDrive\Documents\Python\Projekti\dnevnik_raspolozenja.csv"

# --- Proveri i kreiraj CSV fajl sa zaglavljem ---
if not os.path.exists(FAJL):
    with open(FAJL, "w", newline="", encoding="utf-8") as fajl:
        writer = csv.writer(fajl)
        writer.writerow(["Datum", "Vreme", "Raspolozenje"])

# --- Funkcija za unos raspoloženja ---
def unos_raspolozenja(raspolozenje):
    sada = datetime.now()
    datum = sada.date()
    vreme = sada.strftime("%H:%M:%S")
    with open(FAJL, "a", newline="", encoding="utf-8") as fajl:
        writer = csv.writer(fajl)
        writer.writerow([datum, vreme, raspolozenje])
    messagebox.showinfo("Zapisano", f"Tvoje raspoloženje '{raspolozenje}' je sačuvano!")

# --- Funkcija za statistiku ---
def statistika():
    if not os.path.exists(FAJL):
        return None

    with open(FAJL, "r", encoding="utf-8") as fajl:
        reader = csv.reader(fajl)
        next(reader)  # preskoči header
        raspolozenja = [linija[2] for linija in reader if len(linija) == 3]

    if not raspolozenja:
        return None

    broj_raspolozenja = Counter(raspolozenja)
    ukupno = sum(broj_raspolozenja.values())
    
    print("\nStatistika raspoloženja:")
    for stanje, broj in broj_raspolozenja.items():
        procenat = (broj / ukupno) * 100
        print(f"{stanje}: {broj} dana ({procenat:.1f}%)")
    
    return broj_raspolozenja

# --- Funkcija za personalizovani komentar ---
def komentar(broj_raspolozenja):
    if not broj_raspolozenja:
        messagebox.showinfo("Komentar", "Još nema zapisa za analizu.")
        return

    srecan = broj_raspolozenja.get("srećan", 0)
    tuzan = broj_raspolozenja.get("tužan", 0)
    neutralan = broj_raspolozenja.get("neutralan", 0)
    ukupno = srecan + tuzan + neutralan

    if ukupno == 0:
        messagebox.showinfo("Komentar", "Još nema zapisa za analizu.")
        return

    if srecan / ukupno > 0.5:
        messagebox.showinfo("Komentar", "Super! Većina dana je srećna 🙂")
    elif tuzan / ukupno > 0.5:
        messagebox.showinfo("Komentar", "Čini se da ima više tužnih dana 😕")
    else:
        messagebox.showinfo("Komentar", "Raspoloženje je uglavnom neutralno 🙂")

# --- Funkcija za prikaz grafikona ---
def prikazi_grafikon():
    if not os.path.exists(FAJL):
        messagebox.showinfo("Greška", "Još nema zapisa.")
        return

    with open(FAJL, "r", encoding="utf-8") as fajl:
        reader = csv.reader(fajl)
        next(reader)
        raspolozenja = [linija[2] for linija in reader if len(linija) == 3]

    if not raspolozenja:
        messagebox.showinfo("Greška", "Još nema zapisa.")
        return

    broj_raspolozenja = Counter(raspolozenja)
    
    boje = {"srećan": "green", "tužan": "red", "neutralan": "gray"}
    plt.bar(broj_raspolozenja.keys(), broj_raspolozenja.values(), color=[boje.get(k, "blue") for k in broj_raspolozenja.keys()])
    
    # Dodaj broj iznad stubova
    for i, (stanje, broj) in enumerate(broj_raspolozenja.items()):
        plt.text(i, broj + 0.1, f"{broj}", ha='center')

    plt.title("Raspoloženje tokom vremena")
    plt.ylabel("Broj dana")
    plt.xlabel("Raspoloženje")
    plt.show()

# --- GUI ---
root = tk.Tk()
root.title("Mini dnevnik raspoloženja")
root.geometry("300x250")

tk.Label(root, text="Izaberi svoje raspoloženje:").pack(pady=10)

tk.Button(root, text="Srećan", width=15, command=lambda: unos_raspolozenja("srećan")).pack(pady=5)
tk.Button(root, text="Tužan", width=15, command=lambda: unos_raspolozenja("tužan")).pack(pady=5)
tk.Button(root, text="Neutralan", width=15, command=lambda: unos_raspolozenja("neutralan")).pack(pady=5)
tk.Button(root, text="Prikaži grafikon", width=15, command=prikazi_grafikon).pack(pady=10)
tk.Button(root, text="Prikaži statistiku i komentar", width=25, command=lambda: komentar(statistika())).pack(pady=5)

root.mainloop()
