import pandas as pd

class AnalysisController:
    """
    Verwaltet die Logik der Datenanalyse im Analysefenster.
    Führt Filterung und Berechnung von Min/Max/Durchschnitt aus.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def analyze_data(self):
        """
        Filtert die Daten nach Start- und Enddatum und berechnet Statistiken.
        Zeigt die Ergebnisse im Analysefenster an
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
