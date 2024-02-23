import datetime     # Modul pozwalajacy na operacje na datach
import tkinter as tk    # Biblioteka umozliwiająca tworzenie interfejsu graficznego
import tkcalendar   # Modul do wprowadzania daty z kalendarza
import kalkulator   # Import pliku kalkulator

# Umozliwia uzycie Figure z biblioteki matplotlib jako widget Tk,
# aby wykres byl czescia glownego okna Tk, a nie osobnym oknem
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure    # Import klasy Figure, ktora reprezentuje wykres

import matplotlib.ticker as ticker  # Aby ograniczyc liczbe wpisow na osi czasu (ox)


class AnalizaWalutyUI:
    def __init__(self, root, dostepne_waluty, analiza):
        # https://www.tutorialspoint.com/python/tk_frame.htm#
        self.zakladka = tk.Frame(root)    # Z pakietu tk stworzenie obiektu Frame(zakladka) i podpiecie go do notatnika
        self.analiza = analiza

        # Stworzenie pola wyboru waluty docelowej
        self.waluta_docelowa_wartosc = tk.StringVar(root)
        self.waluta_docelowa_wartosc.set(dostepne_waluty[0])    # Ustawienie wartosci poczatkowej z listy walut
        ## Stworzenie obiektu do wybierania (OptionMenu)
        ## https://www.geeksforgeeks.org/tkinter-optionmenu-widget/
        self.pole_wyboru_waluty = tk.OptionMenu(self.zakladka, self.waluta_docelowa_wartosc, *dostepne_waluty)

        # Tworzy przycisk(Button) z napisem, po nacisnieciu ktorego rysuje sie nowy wykres
        self.przycisk_przelicz = tk.Button(self.zakladka, text="Wyświetl dane waluty z podanego przedziału",
                                           command=self.akcja_nowy_wykres)

        # Stworzenie obiektu wykresu o wymiarach 8 x 6 cali, z rozdzielczoscia 100 pikseli na cal
        self.figure = Figure(figsize=(8, 6), dpi=100)
        # Umozliwienie uzycia Figure z poziomu tkinter
        # https://coderslegacy.com/figurecanvastkagg-matplotlib-tkinter/
        # https://datatofish.com/matplotlib-charts-tkinter-gui/
        self.wykres_jako_obraz_w_tk = FigureCanvasTkAgg(self.figure, self.zakladka)
        # Stworzenie pojedynczego wykresu (jedynego)
        self.osie_wykresu = self.figure.add_subplot(1, 1, 1)

        # https://www.tutorialspoint.com/how-to-justify-text-in-label-in-tkinter-in-python-need-justify-in-tkinter
        # Stworzenie etykiety(Label) wyjustowanej do lewej strony
        self.label_parametry_waluty = tk.Label(self.zakladka, justify="left")

        # Stworzenie dwoch etykiet z opisem daty
        self.label_data_poczatkowa = tk.Label(self.zakladka, text="Data początkowa", justify="right")
        self.label_data_koncowa = tk.Label(self.zakladka, text="Data końcowa", justify="right")


        # https://www.plus2net.com/python/tkinter-DateEntry.php
        # https://www.plus2net.com/python/tkinter-DateEntry-mindate-maxdate.php
        # Stworzenie pol wyboru daty (DateEntry) z pakietu tkcalendar,
        # po kliknieciu na ktory otwiera sie kalendarz
        # minimalna data - 2 stycznia 2002, maksymalna data - dzisiaj
        self.kalendarz_poczatek = tkcalendar.DateEntry(self.zakladka, mindate=datetime.date(2002, 1, 2), maxdate=datetime.date.today())
        # Ustawienie wartosci poczatkowej pola na date 30 dni temu
        self.kalendarz_poczatek.set_date(datetime.date.today()-datetime.timedelta(days=30))
        # https://tkcalendar.readthedocs.io/en/stable/howtos.html
        # Ustawienie formatu daty wyswietlanej w polu
        self.kalendarz_poczatek.configure(date_pattern="yyyy-mm-dd")

        # Analogicznie dla daty koncowej
        self.kalendarz_koniec = tkcalendar.DateEntry(self.zakladka, mindate=datetime.date(2002, 1, 2), maxdate=datetime.date.today())
        self.kalendarz_koniec.set_date(datetime.date.today())
        self.kalendarz_koniec.configure(date_pattern="yyyy-mm-dd")

        # https://www.pythontutorial.net/tkinter/tkinter-grid/
        # pozycje widgetow
        self.przycisk_przelicz.grid(column=2, row=1)
        self.wykres_jako_obraz_w_tk.get_tk_widget().grid(column=2, row=4)
        self.pole_wyboru_waluty.grid(column=1, row=1)
        self.label_parametry_waluty.grid(column=1, row=4)
        self.label_data_poczatkowa.grid(column=1, row=2, sticky="E")
        self.label_data_koncowa.grid(column=1, row=3, sticky="E")
        self.kalendarz_poczatek.grid(column=2, row=2, sticky="W")
        self.kalendarz_koniec.grid(column=2, row=3, sticky="W")

    # Zwraca stworzona zakladke do podpiecia w notatniku
    def zwroc_zakladke(self):
        return self.zakladka

    # Zwraca tytul zakladki
    def tytul(self):
        return "Analiza Waluty"

    # Narysowanie wykresu i wyswietlenie parametrow waluty
    def akcja_nowy_wykres(self):
        #wyczyszczenie poprzedniego wykresu
        self.wyczysc_wykres()
        # zwracamy osobno dwie listy z datami (na os ox) i wartosciami (na os oy)
        daty, wartosci = self.analiza.kursy_z_przedzialu_do_wykresu(self.waluta_docelowa_wartosc.get(),
                                                                    self.kalendarz_poczatek.get_date(),
                                                                    self.kalendarz_koniec.get_date())

        # Plot - podanie nowych danych do wykresu
        self.osie_wykresu.plot(daty, wartosci)

        # https://matplotlib.org/3.4.3/gallery/ticks_and_spines/tick-locators.html
        # Ograniczenie punktów na osi X do max 5 wartości
        self.osie_wykresu.xaxis.set_major_locator(ticker.MaxNLocator(5))

        # Draw - narysowanie wykresu z nowymi danymi z perspektywy tk
        self.wykres_jako_obraz_w_tk.draw()
        # aktualizacja etykiety z parametrami waluty
        nowe_parametry_waluty = self.parametry_waluty(wartosci, self.waluta_docelowa_wartosc.get())
        self.label_parametry_waluty.config(text=nowe_parametry_waluty)

    # Czyszczenie osi, parametrow waluty i wyrysowanie pustego wykresu
    def wyczysc_wykres(self):
        self.osie_wykresu.clear()
        self.wykres_jako_obraz_w_tk.draw()
        # W razie braku danych zostawia komunikat
        self.label_parametry_waluty.config(text="Brak \npoprawnych \ndanych")

    # Obliczanie parametrow waluty, wyswietlanych obok wykresu,
    # zwraca sformatowanego stringa z parametrami
    def parametry_waluty(self, wartosci, waluta):
        # Uzywanie funkcji z pliku kalkulator do obliczania
        srednia = kalkulator.srednia_kursu(wartosci)
        minimalny_kurs, maksymalny_kurs = kalkulator.min_max(wartosci)
        ytd = self.analiza.ytd(waluta)
        # Ustalenie formatu napisu
        formatka_wyniku = "Średnia: {srednia}\nMin: {min}\nMax: {max}\nYTD: {ytd}%"
        return formatka_wyniku.format(srednia=srednia, min=minimalny_kurs, max=maksymalny_kurs, ytd=ytd)

