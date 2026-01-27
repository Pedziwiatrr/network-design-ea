# Optymalizacja wykorzystania zasobów w sieci teleinformatycznej

### Autorzy: Kacper Siemionek, Michał Pędziwiatr

# Wymagania

- Python 3.10 lub nowszy
- Biblioteki zawarte w pliku `requirements.txt`

# Kluczowe pliki

- **`main.py`** - Główny skrypt uruchamiający, dokładne informacje o argumentach wywołania znajdują się w dokumentacji oraz po dodaniu flagi `-h` do wywołania.
- **`src/ea.py`** - Logika algorytmu ewolucyjnego.
- **`src/models.py`** - Definicje struktur danych (węzły, łącza, sieć, zapotrzebowania).
- **`src/config.py`** - Definicje domyślnych wartości.
- **`src/visualization/plotter.py`, `src/visualization/map.py`** - Moduły odpowiedzialne za generowanie wykresów oraz wizualizację mapy sieci.
- **`src/utils/loader.py`** - Parser formatu SNDlib wczytujący dane sieci z folderu `/data`.
- **`src/utils/results_to_csv.py`** - Konwerter wyników działania algorytmu z JSON do csv.
- **`tests/tester.py`** - Roboczy skrypt weryfikujący poprawność wczytywania danych i podstawowych operacji algorytmu ewolucyjnego.
