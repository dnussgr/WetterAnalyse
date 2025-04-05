import tkinter as tk
import asyncio
import pandas as pd

from Model.WeatherModel import WeatherModel
from View.MainView import MainView
from View.PlotHelper import draw_seven_days_plot
from Controller.AnalysisController import AnalysisController

class MainController:
    """
    Hauptcontroller der Anwendung.
    Initialisiert das Modell, die Hauptansicht und verwaltet das Laden
    und Anzeigen der Wetterdaten der letzten 7 Tage.
    """

    def __init__(self):
        self.model = WeatherModel("Data/wetterdaten.csv")
        self.root = tk.Tk()
        self.view = MainView(self.root, self)
        self.analysis = None


    def run(self):
        """
        Startet das Hauptfenster und lädt initial die letzten 7 Tage Wetterdaten.
        """
        asyncio.run(self.load_data())
        self.root.mainloop()


    async def load_data(self):
        """
        Lädt asynchron Daten der letzten sieben Tage, ausgehend vom heutigen Datum.
        Zeigt diese in der Tabelle + im Diagramm.
        """
        data = await self.model.load_data()

        data["Datum"] = pd.to_datetime(data["Datum"], errors="coerce")

        today = pd.Timestamp.today().normalize()
        seven_days_back = today - pd.Timedelta(days=7)
        recent_data = data[(data["Datum"] >= seven_days_back) & (data["Datum"] <= today)]

        self.view.show_data(recent_data)
        draw_seven_days_plot(self.view.plot_frame, recent_data, self.view)


    def open_analysis_window(self):
        """
        Öffnet das Analysefenster und initialisiert AnalysisController,
        sobald die AnalysisView vorhanden ist.
        """
        self.view.create_analysis_window()

        if not self.analysis:
            self.analysis = AnalysisController(self.model, self.view.analysis_view)


    def analyze_data(self):
        """
        Führt eine Analyse über das Analysefenster aus.
        """
        if not self.view.analysis_view:
            return

        self.analysis.view = self.view.analysis_view
        self.analysis.analyze_data()
