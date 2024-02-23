class Kalkulator:

    # Konstuktor, ktory przyjmuje obiekt klasy NbpApi
    def __init__(self, nbp_api):
        self.nbp = nbp_api

    def przelicz_kwote(self, waluta1, waluta2, kwota):
        kursy = self.nbp.pobranie_dwoch_walut_z_daty(waluta1, waluta2)
        # https://stackoverflow.com/questions/9542738/python-find-in-list
        # Szukanie wystapienia zadanej waluty, jesli nie ma zwraca 1 (kurs PLN)
        kurs_waluty1 = next((kurs["mid"] for kurs in kursy if kurs["code"] == waluta1), 1.0)
        kurs_waluty2 = next((kurs["mid"] for kurs in kursy if kurs["code"] == waluta2), 1.0)
        return przeliczanie_kursu(kurs_waluty1, kurs_waluty2, kwota)


# Szukanie minimum i maximum
def min_max(lista_kursow):
    minimum = round(min(lista_kursow), 4)
    maximum = round(max(lista_kursow), 4)
    return minimum, maximum


# Liczenie procentowej zmiany kursu miedzy dwiema wartosciami
def zmiana_kursu(poczatek, koniec):
    zmiana = ((koniec - poczatek) / poczatek) * 100
    return round(zmiana, 4)


# Liczenie sredniej kursu z zadanej listy
def srednia_kursu(lista_kursow):
    srednia = sum(lista_kursow) / len(lista_kursow)
    return round(srednia, 4)


# Przeliczanie kursu jednej waluty w druga
def przeliczanie_kursu(kurs_waluta1, kurs_waluta2, kwota):
    stosunek_kursow = kurs_waluta1 / kurs_waluta2
    nowa_kwota = float(kwota) * stosunek_kursow
    return round(nowa_kwota, 4)
