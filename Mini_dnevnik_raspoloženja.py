# mini_dnevnik.py

from datetime import date
import csv
import os
from collections import Counter
import matplotlib.pyplot as plt

FAJL = r"C:\Users\mirko\OneDrive\Documents\Python\Projekti\dnevnik.csv"

# --- Funkcija za unos raspoloženja ---
def unos_raspolozenja():
    print("\nUnesi svoje raspoloženje za danas:")
    print("Opcije: srećan, tužan, neutralan")
    raspolozenje = input("Tvoje raspoloženje: ").strip().lower()

    if raspolozenje not in ["srećan", "tužan", "neutralan"]:
        print("Nepoznata opcija, pokušaj ponovo.")
        return unos_raspolozenja()

    danas = date.today()
    with open(FAJL, "a", newline="") as fajl:
        writer = csv.writer(fajl)
        writer.writerow([danas, raspolozenje])

    print("Zapisano! Hvala što deliš svoje raspoloženje :)")

# --- Funkcija za prikaz prethodnih unosa ---
def prikaz_prethodnih():
    print("\nTvoje prethodne beleške:")
    if not os.path.exists(FAJL):
        print("Još nema zapisa.")
        return

    with open(FAJL, "r") as fajl:
        reader = csv.reader(fajl)
        zapisi = list(reader)
        if not zapisi:
            print("Još nema zapisa.")
            return
        for linija in zapisi:
            print(f"{linija[0]} -> {linija[1]}")

# --- Funkcija za statistiku raspoloženja ---
def statistika():
    if not os.path.exists(FAJL):
        return None

    with open(FAJL, "r") as fajl:
        reader = csv.reader(fajl)
        raspolozenja = [linija[1] for linija in reader]

    if not raspolozenja:
        return None

    broj_raspolozenja = Counter(raspolozenja)
    ukupno = sum(broj_raspolozenja.values())
    
    print("\nStatistika raspoloženja:")
    for stanje, broj in broj_raspolozenja.items():
        procenat = (broj / ukupno) * 100
        print(f"{stanje}: {broj} dana ({procenat:.1f}%)")
    
    return broj_raspolozenja

# --- Funkcija za prikaz grafikona ---
def prikazi_grafikon(broj_raspolozenja):
    if not broj_raspolozenja:
        return

    plt.bar(broj_raspolozenja.keys(), broj_raspolozenja.values(), color=["green", "red", "gray"])
    plt.title("Raspoloženje tokom vremena")
    plt.ylabel("Broj dana")
    plt.xlabel("Raspoloženje")
    plt.show()

# --- Funkcija za personalizovani komentar ---
def komentar(broj_raspolozenja):
    if not broj_raspolozenja:
        return

    srecan = broj_raspolozenja.get("srećan", 0)
    tuzan = broj_raspolozenja.get("tužan", 0)
    neutralan = broj_raspolozenja.get("neutralan", 0)
    ukupno = srecan + tuzan + neutralan

    if srecan / ukupno > 0.5:
        print("\nSuper! Većina dana je srećna 🙂")
    elif tuzan / ukupno > 0.5:
        print("\nČini se da ima više tužnih dana 😕")
    else:
        print("\nRaspoloženje je uglavnom neutralno 🙂")

# --- Glavni program ---
def main():
    prikaz_prethodnih()
    unos_raspolozenja()
    broj_raspolozenja = statistika()
    komentar(broj_raspolozenja)
    prikazi_grafikon(broj_raspolozenja)

if __name__ == "__main__":
    main()
