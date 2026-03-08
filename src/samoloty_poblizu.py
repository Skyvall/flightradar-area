from fr24sdk.client import Client
from fr24sdk.models.geographic import Boundary
import math
import os
from dotenv import load_dotenv
from tabulate import tabulate
from mapka import generuj_mapke

# Wczytaj zmienne środowiskowe z pliku .env
load_dotenv()

api_token = os.getenv("API_TOKEN")
if not api_token:
    print("Brak API_TOKEN w pliku .env lub zmiennych środowiskowych!")
    exit(1)

try:
    from lokalizacja import koordynaty
except ImportError:
    print("Brak pliku lub zmiennej 'koordynaty' w lokalizacja.py. Upewnij się, że plik istnieje i zawiera zmienną 'koordynaty'.")
    exit(1)

try:
    lat, lon = map(float, koordynaty.split(","))
except Exception as e:
    print(f"Błąd przetwarzania koordynatów: {e}")
    exit(1)

try:
    promien = float(input("Podaj promień wyszukiwania w kilometrach: "))
except ValueError:
    print("Nieprawidłowy promień.")
    exit(1)

# Funkcja do obliczenia bounding box na podstawie środka i promienia (w km)
def bounding_box(lat, lon, radius_km):
    R = 6371.0  
    dlat = (radius_km / R) * (180 / math.pi)
    dlon = (radius_km / R) * (180 / math.pi) / math.cos(lat * math.pi/180)
    north = lat + dlat
    south = lat - dlat
    east = lon + dlon
    west = lon - dlon
    return Boundary(north=north, south=south, west=west, east=east)

client = Client(api_token=api_token)

bounds = bounding_box(lat, lon, promien)

flights = client.live.flight_positions.get_full(bounds=bounds)

headers = [
    "lot", "callsign", "typ", "rejestracja", "szerokość", "długość", "wysokość (ft)", "prędkość (kt)", "wznoszenie/opadanie (ft/min)", "z lotniska", "na lotnisko", "ETA"
]
table = []
for flight in flights.data:
    table.append([
        getattr(flight, "flight", None),
        getattr(flight, "callsign", None),
        getattr(flight, "type", None),
        getattr(flight, "reg", None),
        getattr(flight, "lat", None),
        getattr(flight, "lon", None),
        getattr(flight, "alt", None),
        getattr(flight, "gspeed", None),
        getattr(flight, "vspeed", None),
        getattr(flight, "orig_iata", None),
        getattr(flight, "dest_iata", None),
        getattr(flight, "eta", None),
    ])

print(f"Samoloty w promieniu {promien} km od ({lat}, {lon}):")
print(tabulate(table, headers=headers, tablefmt="grid", stralign="center"))

print(f"Wyliczony bounding box: N={bounds.north}, S={bounds.south}, W={bounds.west}, E={bounds.east}")
print("Pozycje samolotów przekazywane do mapy:")
punkty = [
    (
        getattr(f, "lat", None),
        getattr(f, "lon", None),
        getattr(f, "flight", None),
        getattr(f, "orig_iata", None),
        getattr(f, "dest_iata", None),
        getattr(f, "track", None)
    )
    for f in flights.data
    if getattr(f, "lat", None) is not None and getattr(f, "lon", None) is not None
]
generuj_mapke((lat, lon), punkty)
print("Mapa została zapisana do pliku mapa.html")
