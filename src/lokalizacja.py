from fr24sdk.client import Client
import requests

zgoda = input("Czy mogę automatycznie pobrać Twoję koordynaty GPS?")
if zgoda.lower() == "tak":
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    koordynaty = data.get("loc")
    print(f"Twoja lokalizacja: {koordynaty}")
else:
    lokalizacja = input("Podaj lokalizację ręcznie: ")
    
    

