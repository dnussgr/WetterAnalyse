# WetterAnalyse
Eine interaktive Wetteranalyse-Anwendung mit grafischer Benutzeroberfläche, entwickelt in Python mit `tkinter` &amp; `pandas`.
Sie ermöglicht eine visuelle Auswertung historischer Wetterdaten und bietet Statistiken über definierbare Zeiträume.

## Features

- Analyse von Temperatur, Luftfeuchtigkeit und Luftdruck
- Auswahl eines Zeitraums per Kalender (tkcalendar)
- Berechnung von Minimum, Maximum und Durchschnitt
- Intuitive GUI mit Tabellenansicht (Treeview)
- CSV-Datenquelle (`wetterdaten.csv`)
- Asynchrone Datenverarbeitung (`asyncio`)
- Struktur nach MVC-Prinzip

## Starten

### 1. Vorbereitungen
Python 3.10+ empfohlen. Abhängigkeiten installieren:

```bash
pip install pandas tkcalendar
```
### 2. Starten
```bash
python Main.py
```

## TODO / Ideen
- Diagramm-Visualisierung mit matplotlib oder seaborn
- Unittests für Model & Controller
- Exportfunktion der Analyse (PDF, Excel)
- Anbindung an eine Wetter-API (OpenWeather, DWD)
