import tkinter as tk    # Biblioteka umozliwiająca tworzenie interfejsu graficznego
from tkinter import ttk     # Bbilioteka zawierajaca notatnik z zakladkami

# Import klas z projektu
from analizaWalutyUI import AnalizaWalutyUI
from kalkulatorKursowUI import KalkulatorKursowUI


class PgGui:

    def __init__(self, dostepneWaluty, kalkulator, analiza):
        self.root = tk.Tk()            # Stworzenie okna aplikacji
        # https://www.pythontutorial.net/tkinter/tkinter-notebook/
        self.notatnik = ttk.Notebook(self.root)     # Stworzenie notatnika z zakladkami w oknie aplikacji

        # Stworzenie dwoch obiektow do stworzenia zakladek
        kalkulator_kursow = KalkulatorKursowUI(self.notatnik, dostepneWaluty, kalkulator)
        analiza_waluty = AnalizaWalutyUI(self.notatnik, dostepneWaluty, analiza)

        # Dodanie zakladek do notatnika
        self.notatnik.add(kalkulator_kursow.zwroc_zakladke(), text=kalkulator_kursow.tytul())
        self.notatnik.add(analiza_waluty.zwroc_zakladke(), text=analiza_waluty.tytul())

        # Wyswietl
        self.notatnik.pack()

    # Uruchomienie aplikacji w Tk
    def start(self):
        self.root.mainloop()
