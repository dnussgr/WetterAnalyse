import tkinter as tk
from tkinter import ttk, PhotoImage
from tkcalendar import DateEntry

class WeatherView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Wetteranalyse")
        self.root.geometry("900x500")
        self.icon = PhotoImage(file="Data/icon.png")
        self.root.iconphoto(False, self.icon)

        # Initialisierungen
        self.label= None
        self.tree = None
        self.button_analysis = None
        self.start_date = None
        self.end_date = None
        self.button_analyse = None
        self.result_label = None
        self.analysis_window = None
        self.stats_labels = None
        self.tree_analysis = None

        self.create_gui()


    def create_gui(self):
        """
        Erstellt das Hauptfenster(root) und zeigt die Daten der letzten Woche in einer Tabelle an
        """

        # Überschrift
        self.label = tk.Label(self.root, text="Wetterdaten der letzten Woche", font=("Helvetica", 18, "bold"))
        self.label.pack(pady=10)

        # Tabelle
        self.tree = ttk.Treeview(self.root, columns=("Datum", "Temperatur (°C)", "Luftfeuchtigkeit (%)", "Luftdruck(hPa)"), show="headings")

        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=120)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Button, der Analyse-Fenster öffnet
        self.button_analysis = tk.Button(self.root, text="Analyse öffnen", command=self.controller.open_analysis_window)
        self.button_analysis.pack(pady=10)


    def show_data(self, data):
        """
        Lädt die Daten für Datum, Temperatur, Luftfeuchtigkeit, Luftdruck
        :param data: die Liste mit den aus der csv-Datei geladenen Daten
        """

        # Vorhandene Reihen werden gelöscht
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Gibt Daten aus
        for index, row in data.iterrows():
            datum = row["Datum"].strftime("%d.%m.%Y")
            self.tree.insert("", tk.END, values=(datum, row["Temperatur"], row["Luftfeuchtigkeit"], row["Luftdruck"]))


    def create_analysis_window(self):
        """
        Erstellt ein Fenster für die Datenanalyse.
        Hier kann ein Anfangs- und Enddatum ausgewählt werden, auf dessen Grundlage dann Min/Max/Durchschnittswerte
        berechnet und die Daten für den gewählten Zeitraum angezeigt werden.
        """

        # Prüft, ob Fenster bereits existiert und hebt es hervor
        if self.analysis_window and self.analysis_window.winfo_exists():
            self.analysis_window.lift()
            return

        # Fenstereigenschaften
        self.analysis_window = tk.Toplevel(self.root)
        self.analysis_window.title("Datenanalyse")
        self.analysis_window.geometry("650x500")
        self.icon = PhotoImage(file="Data/icon.png")
        self.analysis_window.iconphoto(False, self.icon)

        # Grid-Container für Statistikwerte
        stats_frame = tk.Frame(self.analysis_window)
        stats_frame.pack(fill="x", padx=10, pady=5)

        # Überschriften für Statistik-Grid
        labels = ["", "Temperatur", "Luftfeuchtigkeit", "Luftdruck"]
        for column, text in enumerate(labels):
            tk.Label(stats_frame, text=text, font=("Helvetica", 10, "bold"), borderwidth=2, relief="flat", width=15).grid(
                row=0, column=column)

        self.stats_labels = {}
        row_labels = ["Min", "Max", "Durchschnitt"]

        for row, row_text in enumerate(row_labels, start=1):

            tk.Label(stats_frame, text=row_text, font=("Helvetica", 10), borderwidth=2, relief="flat", width=15).grid(
                row=row, column=0)

            # Label für Temperatur, Luftfeuchtigkeit, Luftdruck
            for column in range(1, 4):
                label = tk.Label(stats_frame, text="---", font=("Helvetica", 10), borderwidth=2, relief="flat", width=15)
                label.grid(row=row, column=column)
                self.stats_labels[(row, column)] = label

        # TreeView für alle Werte im gewählten Zeitraum
        columns = ("Datum", "Temperatur", "Luftfeuchtigkeit", "Luftdruck")
        self.tree_analysis = ttk.Treeview(self.analysis_window, columns=columns, show="headings")

        for column in columns:
            self.tree_analysis.heading(column, text=column)
            self.tree_analysis.column(column, width=150, anchor="center")

        self.tree_analysis.pack(fill="both", expand=True, padx=10, pady=5)

        # Start- und Enddatumsauswahl
        date_frame = tk.Frame(self.analysis_window)
        date_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(date_frame, text="Startdatum:").pack(side="left")
        self.start_date = DateEntry(date_frame, width=12)
        self.start_date.pack(side="left", padx=5)

        tk.Label(date_frame, text="Enddatum:").pack(side="left")
        self.end_date = DateEntry(date_frame, width=12)
        self.end_date.pack(side="left", padx=5)

        # Analyse-Button
        self.button_analyse = tk.Button(date_frame, text="Analysieren", command=self.controller.analyze_data)
        self.button_analyse.pack(side="left", padx=10)


    def show_analysis_result(self, result, all_filtered_values):
        """
        Zeigt die Analyseergebnisse in der Tabelle und aktualisiert die Statistikwerte
        :param result: das Ergebnis der Analyse für den ausgewählten Zeitraum
        :param all_filtered_values: Liste mit allen gefilterten Daten
        """

        # Aktualisiert die Statistik-Werte
        if result:
            statistics_values = [
                ["Min", result["Temperatur"]["Min"], result["Luftfeuchtigkeit"]["Min"], result["Luftdruck"]["Min"]],
                ["Max", result["Temperatur"]["Max"], result["Luftfeuchtigkeit"]["Max"], result["Luftdruck"]["Max"]],
                ["Durchschnitt", result["Temperatur"]["Durchschnitt"], result["Luftfeuchtigkeit"]["Durchschnitt"],
                 result["Luftdruck"]["Durchschnitt"]],
            ]

            for row_index, row_data in enumerate(statistics_values, start=1):
                for col_index in range(1, 4):
                    self.stats_labels[(row_index, col_index)].config(text=f"{row_data[col_index]:.2f}")

        # Löscht zuerst alle vorhandenen Werte, liest neue Werte ein und gibt sie aus
        for row in self.tree_analysis.get_children():
            self.tree_analysis.delete(row)

        for _, row in all_filtered_values.iterrows():
            datum = row["Datum"].strftime("%d.%m.%Y")
            self.tree_analysis.insert("", tk.END, values=(datum,
                                                          row["Temperatur"],
                                                          row["Luftfeuchtigkeit"],
                                                          row["Luftdruck"]))



