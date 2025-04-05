import tkinter as tk
from tkinter import ttk, PhotoImage
from View.AnalysisView import AnalysisView

class MainView:
    """
    Verwaltet das Hauptfenster, das die Wetterdaten der letzten Woche
    als Tabelle und Temperaturdiagramm anzeigt.
    """

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Wetteranalyse")
        self.root.geometry("1050x500")
        self.root.configure(bg="white")
        self.icon = PhotoImage(file="Data/icon.png")
        self.root.iconphoto(False, self.icon)

        # GUI-Komponenten
        self.label = None
        self.tree = None
        self.plot_frame = None
        self.canvas = None
        self.button_analysis = None
        self.analysis_view = None

        self.create_gui()

    def create_gui(self):
        """
        Erstellt das Hauptfenster (root) mit TreeView für Wetterdaten
        und einem Seaborn-Plot daneben.
        """

        # Überschrift
        self.label = tk.Label(self.root, text="Wetterdaten der letzten Woche", font=("Helvetica", 18, "bold"), bg="white")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # Grid-Konfiguration
        self.root.grid_columnconfigure(0, weight=1)   # Tabelle
        self.root.grid_columnconfigure(1, weight=1)   # Plot
        self.root.grid_rowconfigure(1, weight=1)      # Tree + Plot

        # TreeView-Tabelle
        self.tree = ttk.Treeview(self.root,
                                 columns=("Datum", "Temperatur (°C)", "Luftfeuchtigkeit (%)", "Luftdruck(hPa)"),
                                 show="headings")

        column_widths = {
            "Datum": 80,
            "Temperatur (°C)": 100,
            "Luftfeuchtigkeit (%)": 120,
            "Luftdruck(hPa)": 120
        }

        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
            self.tree.column(column, minwidth=column_widths[column], width=column_widths[column], anchor="center",
                             stretch=True)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))

        # Plotbereich
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))

        # Button zum Öffnen der Analyse
        self.button_analysis = tk.Button(self.root, text="Analyse öffnen", command=self.controller.open_analysis_window)
        self.button_analysis.grid(row=2, column=0, columnspan=2, pady=(0, 10))


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
        Erstellt das Analyse-Fenster mit Datumsauswahl, Statistik und Plot.
        """
        if self.analysis_view is None:
            self.analysis_view = AnalysisView(self.root, self.controller)
        self.analysis_view.create_analysis_window()


    def show_analysis_result(self, result, all_filtered_values):
        """
        Gibt Analyseergebnisse aus dem Controller an die AnalysisView weiter.
        """
        if self.analysis_view:
            self.analysis_view.show_analysis_result(result, all_filtered_values)
