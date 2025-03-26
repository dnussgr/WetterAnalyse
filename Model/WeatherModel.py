import pandas as pd
import asyncio

class WeatherModel:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None


    async def load_data(self):
        """
        Lädt die CSV-Datei asynchron
        :return: eine Liste mit den Wetterdaten
        """
        loop = asyncio.get_event_loop()
        self.data = await loop.run_in_executor(None, pd.read_csv, self.filepath)
        self.data["Datum"] = pd.to_datetime(self.data["Datum"])
        return self.data


    def filter_data_timespan(self, start_date, end_date):
        """
        Filtert Wetterdaten nach einem gegebenen Zeitraum.
        :param start_date: Anfangsdatum der Analyse
        :param end_date: Enddatum der Analyse
        :return: die Liste mit gefilterten Daten
        """
        if self.data is None:
            return None

        self.data["Datum"] = pd.to_datetime(self.data["Datum"], errors="coerce")

        # Konvertierung von start/end_date zu Pandas-Timestamp
        if isinstance(start_date, pd.Timestamp) is False:
            start_date = pd.Timestamp(start_date)
        if isinstance(end_date, pd.Timestamp) is False:
            end_date = pd.Timestamp(end_date)

        # Entfernt zur Sicherheit alle Null-Werte in der Liste
        filtered_data = self.data.dropna(subset=["Datum"])

        return filtered_data[(filtered_data["Datum"] >= start_date) & (filtered_data["Datum"] <= end_date)]


    @staticmethod
    def calculate_statistics(filtered_data):
        """
        Berechnet die Durchschnittswerte des gefilterten Zeitraums
        :param filtered_data: die Liste mit den Daten aus dem gefilteren Zeitraum
        :return: das statistics-Dictionary mit den Werten für Temperatur, Luftfeuchte und Luftdruck
        """
        if filtered_data is None or filtered_data.empty:
            return None

        statistics = {
            "Temperatur": {
                "Min": filtered_data["Temperatur"].min(),
                "Max": filtered_data["Temperatur"].max(),
                "Durchschnitt": filtered_data["Temperatur"].mean()
            },
            "Luftfeuchtigkeit": {
                "Min": filtered_data["Luftfeuchtigkeit"].min(),
                "Max": filtered_data["Luftfeuchtigkeit"].max(),
                "Durchschnitt": filtered_data["Luftfeuchtigkeit"].mean()
            },
            "Luftdruck": {
                "Min": filtered_data["Luftdruck"].min(),
                "Max": filtered_data["Luftdruck"].max(),
                "Durchschnitt": filtered_data["Luftdruck"].mean()
            }
        }
        return statistics
