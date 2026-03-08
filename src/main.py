import os
from dotenv import load_dotenv
import subprocess

# zmienne srodowiskowe dla ukrycia API - tylko w glownym pliku
load_dotenv()


def main():
    print("Witaj w aplikacji FlightRadar!")
    print("Co chcesz zrobić?")
    print("1. Sprawdź lot")
    print("2. Sprawdź loty w pobliżu")
    print("3. Sprawdź lotnisko")
    print("4. Wyjdź")

    choice = input("Wybierz opcję (1-4): ")

    if choice == "1":
        print("Wybrano: Sprawdź lot")
        subprocess.run(["python", "src/loty_poblizu.py"])
    elif choice == "2":
        print("Wybrano: Sprawdź loty w pobliżu")
        subprocess.run(["python", "src/samoloty_poblizu.py"])
    elif choice == "3":
        print("Wybrano: Sprawdź lotnisko")
        subprocess.run(["python", "src/lotnisko.py"])
    elif choice == "4":
        print("Do zobaczenia!")
    else:
        print("Nieprawidłowa opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    main()
