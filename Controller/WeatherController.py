import tkinter as tk
import asyncio
import pandas as pd
from Model.WeatherModel import WeatherModel
from View.WeatherView import WeatherView


class WeatherController:
    def __init__(self):
        self.model = WeatherModel("Data/wetterdaten.csv")
        self.root = tk.Tk()
        self.view = WeatherView(self.root, self)


    def run(self):
        """
        Startet das Laden der csv-Datei und das Hauptfenster
        """
        asyncio.run(self.load_data())
        self.root.mainloop()


    async def load_data(self):
        """
        Lädt asynchron Daten der letzten sieben Tage, ausgehend vom heutigen Datum
        """
        data = await self.model.load_data()

        data["Datum"] = pd.to_datetime(data["Datum"], errors="coerce")

        today = pd.Timestamp.today().normalize()
        seven_days_back = today - pd.Timedelta(days=7)
        recent_data = data[(data["Datum"] >= seven_days_back) & (data["Datum"] <= today)]

        self.view.show_data(recent_data)
        self.view.draw_lineplot(recent_data)


    def open_analysis_window(self):
        self.view.create_analysis_window()


    def analyze_data(self):
        """
        Filtert die Daten nach Start- und Enddatum und berechnet Statistiken
        """
        start = self.view.start_date.get_date()
        end = self.view.end_date.get_date()

        # Ruft gefilterte Daten auf
        filtered_data = self.model.filter_data_timespan(start, end)

        # Falls keine Daten gefunden werden, wird nur ein leerer Frame angezeigt und abgebrochen
        if filtered_data is None or filtered_data.empty:
            self.view.show_analysis_result(None, pd.DataFrame())
            return

        # Berechnet Statistiken
        result = self.model.calculate_statistics(filtered_data)

        # Zeigt Ergebnisse im Analysis-Fenster an
        self.view.show_analysis_result(result, filtered_data)
