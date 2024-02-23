import datetime     # Modul pozwalajacy na operacje na datach
from kalkulator import zmiana_kursu     # Import funkcji z pliku kalkulator


class Analiza:

    # Konstuktor, ktory przyjmuje obiekt klasy NbpApi
    def __init__(self, nbpApi):
        self.nbp = nbpApi

    # Pobiera kursy zadanej waluty z zadanego przedzialu i zwraca osobno w listach daty i wartości
    def kursy_z_przedzialu_do_wykresu(self, waluta, poczatek, koniec):
        kursy_z_przedzialu = self.nbp.pobranie_waluty_z_przedzialu(waluta, poczatek, koniec)

        # List comprehension
        daty = [kurs["effectiveDate"] for kurs in kursy_z_przedzialu]
        wartosci = [kurs["mid"] for kurs in kursy_z_przedzialu]
        return daty, wartosci

    # Liczenie zmiany kursu od poczatku roku
    def ytd(self, waluta):
        kurs_aktualny = self.nbp.pobranie_aktualnego_kursu(waluta)
        # Metoda today zwraca dzisiejsza date, bierzemy z niej tylko rok
        aktualny_rok = datetime.date.today().year

        # https://www.programiz.com/python-programming/datetime/strftime
        # Data pierwszego dnia biezacego roku jako string w odpowiednim formacie
        pierwszy_dzien_roku = datetime.date(aktualny_rok, 1, 1).strftime("%Y-%m-%d")

        # Pobiera kursy waluty z przedzialu od poczatku roku do dzisiaj,
        # zeby potem wybrac pierwszy ktory bedzie dostepny w danym roku
        kursy_od_poczatku_roku = self.nbp.pobranie_waluty_z_przedzialu(waluta, pierwszy_dzien_roku)
        pierwszy_dostepny_kurs_w_roku = kursy_od_poczatku_roku[0]["mid"]

        return zmiana_kursu(pierwszy_dostepny_kurs_w_roku, kurs_aktualny)
