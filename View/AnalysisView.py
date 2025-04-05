import tkinter as tk
from tkinter import ttk, PhotoImage
from tkcalendar import DateEntry
from View.PlotHelper import draw_analysis_plots
from View.PopupHelper import force_popup_above

class AnalysisView:
    """
    Stellt ein separates Analysefenster dar, in dem Zeiträume gewählt,
    Statistiken berechnet und Diagramme angezeigt werden.
    """

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.analysis_window = None

        # UI-Komponenten
        self.start_date = None
        self.end_date = None
        self.stats_labels = {}
        self.tree_analysis = None
        self.plot_frame_analysis = None
        self.button_analyse = None

    def create_analysis_window(self):
        """
        Erstellt ein Fenster für die Datenanalyse
        """

        if self.analysis_window and self.analysis_window.winfo_exists():
            self.analysis_window.lift()
            return

        # Fenstereigenschaften
        self.analysis_window = tk.Toplevel(self.root)
        self.analysis_window.title("Datenanalyse")
        self.analysis_window.geometry("1320x920")
        self.analysis_window.config(bg="white")
        self.analysis_window.iconphoto(False, PhotoImage(file="Data/icon.png"))

        # TreeView-Design auf Weiß umstellen
        style = ttk.Style()
        style.configure("Treeview", background="white", fieldbackground="white", foreground="black")

        # Grid-Konfiguration
        self.analysis_window.grid_columnconfigure(0, weight=0)
        self.analysis_window.grid_columnconfigure(1, weight=1)
        self.analysis_window.grid_rowconfigure(1, weight=1)

        # Statistikbereich (oben links)
        stats_frame = tk.Frame(self.analysis_window, bg="white")
        stats_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))

        labels = ["", "Temperatur", "Luftfeuchtigkeit", "Luftdruck"]
        for col, text in enumerate(labels):
            tk.Label(stats_frame, text=text, font=("Helvetica", 10, "bold"), width=15, bg="white").grid(row=0, column=col)

        row_labels = ["Min", "Max", "Durchschnitt"]
        for r, row_text in enumerate(row_labels, start=1):
            tk.Label(stats_frame, text=row_text, font=("Helvetica", 10), width=15, bg="white").grid(row=r, column=0)
            for c in range(1, 4):
                label = tk.Label(stats_frame, text="---", font=("Helvetica", 10), width=15, bg="white")
                label.grid(row=r, column=c)
                self.stats_labels[(r, c)] = label

        # TreeView-Tabelle
        columns = ("Datum", "Temperatur", "Luftfeuchtigkeit", "Luftdruck")
        self.tree_analysis = ttk.Treeview(self.analysis_window, columns=columns, show="headings")

        column_widths = {
            "Datum": 50,
            "Temperatur": 50,
            "Luftfeuchtigkeit": 50,
            "Luftdruck": 50
        }
        for col in columns:
            self.tree_analysis.heading(col, text=col)
            self.tree_analysis.column(col, width=column_widths[col], anchor="center")

        self.tree_analysis.grid(row=1, column=0, sticky="nsew", padx=10, pady=(10, 5))

        # Kalender und Button
        date_frame = tk.Frame(self.analysis_window, bg="white")
        date_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        tk.Label(date_frame, text="Startdatum:", bg="white").pack(side="left")
        self.start_date = DateEntry(date_frame, width=12, locale="de_DE", date_pattern="dd.mm.yyyy")
        self.start_date.pack(side="left", padx=5)

        tk.Label(date_frame, text="Enddatum:", bg="white").pack(side="left")
        self.end_date = DateEntry(date_frame, width=12, locale="de_DE", date_pattern="dd.mm.yyyy")
        self.end_date.pack(side="left", padx=5)

        self.button_analyse = tk.Button(date_frame, text="Analysieren", command=self.controller.analyze_data)
        self.button_analyse.pack(side="left", padx=10)

        # Kalender-Popup immer oberhalb anzeigen
        force_popup_above(self.start_date)
        force_popup_above(self.end_date)

        # Plotbereich rechts
        self.plot_frame_analysis = tk.Frame(self.analysis_window, bg="white")
        self.plot_frame_analysis.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=(5, 10), pady=10)


    def show_analysis_result(self, result, all_filtered_values):
        """
        Zeigt die Analyseergebnisse in der Tabelle und aktualisiert die Statistikwerte.
        """

        # Tabelle aktualisieren
        for row in self.tree_analysis.get_children():
            self.tree_analysis.delete(row)

        for _, row in all_filtered_values.iterrows():
            datum = row["Datum"].strftime("%d.%m.%Y")
            self.tree_analysis.insert("", tk.END, values=(datum,
                                                          row["Temperatur"],
                                                          row["Luftfeuchtigkeit"],
                                                          row["Luftdruck"]))

        # Statistikfelder
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

            draw_analysis_plots(all_filtered_values, result, self.plot_frame_analysis)
