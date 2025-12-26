# Projekt SPDB

## Autorzy

- Nel Kułakowska
- Marcin Wawrzyniak

## Konfiguracja

### Server

Python 3.11.0 + zależności z pliku `requiremets.txt`

1. Sklonować repozytorium do wybranego folderu i przejść do folderu `server`.
2. Utworzyć nowe środowisko wirtualne komendą:

```
python -m venv venv
```

3. Aktywować środowisko.
4. Zainstalować wymagane zależności komendą:

```
pip install -r ./requirements.txt
```

5. Zweryfikować poprawność konfiguracji uruchamiając testy:

```
pytest
```

## Przydatne linki

- **osmnx**: https://osmnx.readthedocs.io/en/stable/index.html
  - biblioteka obsługująca API OpenStreetMap
- **networkx**: https://networkx.org/

  - osmnx używa obiektów z tej biblioteki do reprezentacji grafów, potrzebne do implementacji algorytmu

- **folium**: https://python-visualization.github.io/folium/latest/
  - wizualizacja na mapie
