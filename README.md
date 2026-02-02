# Optymalizacja wykorzystania zasobów w sieci teleinformatycznej

### Autorzy: Kacper Siemionek, Michał Pędziwiatr

# Wymagania

- Python 3.10 lub nowszy
- Biblioteki zawarte w pliku `requirements.txt`

### Instalacja zależności

```bash
pip install -r requirements.txt
```

# Uruchomienie

### Główna symulacja

Główny skrypt ładujący dane oraz uruchamiający algorytm ewolucyjny:

```bash
python3 main.py
```

Aby zobaczyć dostępne parametry konfiguracji:

```bash
python3 main.py --help
```

### Wizualizacja

Skrypt generujący wykresy zbieżności, czasu działania oraz najniższego kosztu:

```bash
python3 src/visualization/plotter.py [--file INPUT_RESULTS_FILE]
```

Narzędzie do wizualizacji obciążenia na mapie łączy:

```bash
python3 src/visualization/map.py
```

Aby zobaczyć dostępne parametry konfiguracji (skrypt uruchamia nową symulację)

```bash
python3 src/visualization/map.py -h
```

### Testy

Weryfikacja poprawności działania podstawowych modułów

```bash
python3 tests/tester.py
```

# Kluczowe pliki

- **`main.py`** - Główny skrypt uruchamiający, dokładne informacje o argumentach wywołania znajdują się w dokumentacji oraz po dodaniu flagi `-h` do wywołania.
- **`src/ea.py`** - Logika algorytmu ewolucyjnego.
- **`src/models.py`** - Definicje struktur danych (węzły, łącza, sieć, zapotrzebowania).
- **`src/config.py`** - Definicje domyślnych wartości.
- **`src/visualization/plotter.py`, `src/visualization/map.py`** - Moduły odpowiedzialne za generowanie wykresów oraz wizualizację mapy sieci.
- **`src/utils/loader.py`** - Parser formatu SNDlib wczytujący dane sieci z folderu `/data`.
- **`src/utils/results_to_csv.py`** - Konwerter wyników działania algorytmu z JSON do csv.
- **`tests/tester.py`** - Pomocniczy skrypt weryfikujący poprawność wczytywania danych i podstawowych operacji algorytmu ewolucyjnego.
