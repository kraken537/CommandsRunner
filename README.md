# Command Runner

Command Runner to aplikacja napisana w Pythonie, która umożliwia uruchamianie różnych poleceń systemowych za pomocą interfejsu graficznego. Aplikacja obsługuje dwa języki: polski (PL) i angielski (EN).

## Funkcje

- Uruchamianie poleceń systemowych z listy.
- Wyszukiwanie poleceń w czasie rzeczywistym.
- Zmiana języka interfejsu między polskim a angielskim.
- Automatyczne uruchamianie aplikacji z uprawnieniami administratora.
- Usuwanie tymczasowych plików po zamknięciu aplikacji.

## Wymagania

- Python 3.x
- Tkinter
- ctypes
- subprocess
- json
- atexit

## Instalacja

1. Sklonuj repozytorium:
    ```sh
    git clone https://github.com/yourusername/command-runner.git
    cd command-runner
    ```

2. Upewnij się, że masz zainstalowane wymagane biblioteki:
    ```sh
    pip install -r requirements.txt
    ```

## Uruchomienie

1. Uruchom aplikację:
    ```sh
    python main.py
    ```

2. Aplikacja automatycznie uruchomi się z uprawnieniami administratora.

## Zmiana języka

- Aby zmienić język interfejsu, kliknij przycisk "EN" lub "PL" w prawym górnym rogu aplikacji. Aplikacja uruchomi się ponownie z wybranym językiem.

## Struktura projektu

- `main.py` - główny plik aplikacji.
- `commandsPL.json` - plik JSON zawierający listę poleceń w języku polskim.
- `commandsEN.json` - plik JSON zawierający listę poleceń w języku angielskim.
- `icon.ico` - ikona aplikacji.

## Autor

Kuzyn Entertaiment Production

## Licencja

Ten projekt jest licencjonowany na warunkach licencji MIT. Szczegóły znajdują się w pliku LICENSE.
