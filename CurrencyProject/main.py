# Importowanie plikow
import analiza
import kalkulator

# Importowanie klas z plikow
from pggui import PgGui
from nbpapi import NbpApi

# Stworzenie nowego obiektu klasy NbpApi
nbp = NbpApi()

# Tworzenie obiektu klasy pg_gui, do ktorego przekazujemy liste dostepnych walut, nowy obiekt klasy Kalkulator
# i nowy obiekt klasy Analiza
aplikacja = PgGui(nbp.pobranie_dostepnych_walut(), kalkulator.Kalkulator(nbp), analiza.Analiza(nbp))
aplikacja.start()

