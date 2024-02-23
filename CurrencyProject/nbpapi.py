import datetime  # Modul pozwalajacy na operacje na datach
import requests  # Modul pozwalajacy na wysylanie zapytan HTTP


# Klasa obslugujaca komunikacje z interfejsem http z api.nbp.pl
class NbpApi:
    # Zmienne w klasie
    url_aktualne_kursy = "http://api.nbp.pl/api/exchangerates/tables/a/?format=json"
    url_waluta_z_przedzialu = "http://api.nbp.pl/api/exchangerates/rates/a/{code}/{startDate}/{endDate}/?format=json"

    def pobranie_dwoch_walut_z_daty(self, waluta1, waluta2):
        # Wejscie przyklad https://api.nbp.pl/api/exchangerates/tables/a/?format=json
        aktualne_kursy = self.pobranie_aktualnych_kursow()

        # Szuka kursu zadanych walut w liscie ze slownikami, dopisuje do pustej listy
        wynik = []
        for kurs in aktualne_kursy:
            if waluta1 == kurs["code"] or waluta2 == kurs["code"]:
                wynik.append(kurs)
        return wynik

    def pobranie_waluty_z_przedzialu(self, waluta, poczatek, koniec=None):
        # wejscie przyklad: http://api.nbp.pl/api/exchangerates/rates/a/gbp/2012-01-01/2012-01-31/?format=json
        if koniec == None or koniec == "":
            # Przy braku danych o koncu uzywanie dzisiejszego dnia jako konca
            koniec = datetime.date.today().strftime("%Y-%m-%d")
            # Z modulu datetime, klasa date, metoda today zwraca dzisiejsza date, metoda strftime konwertuje do
            # string w podanym formacie https://www.programiz.com/python-programming/datetime/strftime

        url = self.url_waluta_z_przedzialu.format(code=waluta, startDate=poczatek, endDate=koniec)
        # https://realpython.com/python-requests/#the-response
        response = self.wywolaj_api_nbp(url)

        # Odpowiedz nbp konwertuje do postaci data, wartosc
        # Do pustej listy dopisuje slowniki, ktore skladaja sie z daty i kursu waluty
        wynik = []
        for kurs in response["rates"]:
            wynik.append({"effectiveDate": kurs["effectiveDate"], "mid": kurs["mid"]})
        return wynik

    # Pobranie listy dostepnych walut
    def pobranie_dostepnych_walut(self):
        # dopisuje kody walut do pustej listy
        wynik = []
        for kurs in self.pobranie_aktualnych_kursow():
            wynik.append(kurs["code"])
        return wynik

    # Pobiera aktualny kurs danej waluty
    def pobranie_aktualnego_kursu(self, waluta):
        kursy = self.pobranie_aktualnych_kursow()
        wynik = 0
        for kurs in kursy:
            if kurs["code"] == waluta:
                wynik = kurs["mid"]
        return wynik

    # Pobiera aktualne kursy wszystkich dostepnych walut
    def pobranie_aktualnych_kursow(self):
        # wejscie przyklad http://api.nbp.pl/api/exchangerates/tables/a/?format=json
        url = self.url_aktualne_kursy
        response = self.wywolaj_api_nbp(url)

        # Do pustej listy dopisuje slowniki skladajace sie z kodu i kursu waluty
        wynik = []
        for kurs in response[0]["rates"]:
            wynik.append({"code": kurs["code"], "mid": kurs["mid"]})
        return wynik

    # Pobranie danych z danego adresu url w formacie json
    # https://realpython.com/python-requests/#the-get-request
    def wywolaj_api_nbp(self, url):
        return requests.get(url).json()
