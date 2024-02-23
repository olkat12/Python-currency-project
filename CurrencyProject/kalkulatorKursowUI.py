import tkinter as tk    # Biblioteka umozliwiająca tworzenie interfejsu graficznego


# Klasa, ktora tworzy elementy UI i ich obsluge dla kalkulatora
class KalkulatorKursowUI:
    def __init__(self, root, dostepneWaluty, kalkulator):
        # Dodanie do listy dostępnych walut PLN
        waluty_z_pln = ["PLN"] + dostepneWaluty

        # https://www.tutorialspoint.com/python/tk_frame.htm#
        self.zakladka = tk.Frame(root)   # Z pakietu tk stworzenie obiektu Frame(zakladka) i podpiecie go do notatnika
        self.kalkulator = kalkulator

        # Stworzenie pola wyboru waluty zrodlowej
        self.waluta_zrodlowa_wartosc = tk.StringVar(root)
        self.waluta_zrodlowa_wartosc.set(waluty_z_pln[2])     # Ustawienie wartosci poczatkowej z listy walut
        ## Stworzenie obiektu do wybierania (OptionMenu)
        ## https://www.geeksforgeeks.org/tkinter-optionmenu-widget/
        self.pole_wyboru_waluty_zrodlowej = tk.OptionMenu(self.zakladka, self.waluta_zrodlowa_wartosc, *waluty_z_pln)

        # Analogicznie stworzenie pola wyboru waluty docelowej
        self.waluta_docelowa_wartosc = tk.StringVar(root)
        self.waluta_docelowa_wartosc.set(waluty_z_pln[8])
        self.pole_wyboru_waluty_docelowej = tk.OptionMenu(self.zakladka, self.waluta_docelowa_wartosc, *waluty_z_pln)

        # https://stackoverflow.com/questions/16373887/how-to-set-the-text-value-content-of-an-entry-widget-using-a-button-in-tkinter
        # Wartosc poczatkowa dla pola z kwota
        self.kwota_wejsciowa_wartosc = tk.StringVar(root, value="100")
        # Stworzenie pola(Entry) do wpisywania kwoty
        self.pole_kwota_wejsciowa = tk.Entry(self.zakladka, textvariable=self.kwota_wejsciowa_wartosc)

        # Stworzenie etykiety(Label), gdzie pozniej wypisywany jest przeliczony wynik
        self.label_kwota_wyjsciowa = tk.Label(self.zakladka, text="Wybierz obie waluty i kwotę")

        self.przerwa = tk.Label(self.zakladka, text="  ==>  ")

        # Stworzenie przycisku(Button) do uruchamiania przeliczania kwoty
        self.przycisk_przelicz = tk.Button(self.zakladka, text="Przelicz Kwotę", command=self.akcja_przelicz_kwote)

        # https://www.pythontutorial.net/tkinter/tkinter-grid/
        # pozycje widgetow
        self.pole_kwota_wejsciowa.grid(column=1, row=1)
        self.pole_wyboru_waluty_zrodlowej.grid(column=2, row=1)
        self.przerwa.grid(column=3, row=1)
        self.przycisk_przelicz.grid(column=3, row=2)
        self.pole_wyboru_waluty_docelowej.grid(column=4, row=1)
        self.label_kwota_wyjsciowa.grid(column=5, row=1)

    # Zwraca stworzona zakladke do podpiecia w notatniku
    def zwroc_zakladke(self):
        return self.zakladka

    # Zwraca tytul zakladki
    def tytul(self):
        return "Kalkulator Kursow"

    # Przeliczenie kwot
    def akcja_przelicz_kwote(self):
        wynik = self.kalkulator.przelicz_kwote(self.waluta_zrodlowa_wartosc.get(), self.waluta_docelowa_wartosc.get(),
                                               self.kwota_wejsciowa_wartosc.get())
        self.label_kwota_wyjsciowa.config(text=wynik)
        # Zamiana napisu w zakladce na wynik ktory zostal obliczony
        # https://www.geeksforgeeks.org/how-to-change-the-tkinter-label-text/
