import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

def draw_seven_days_plot(plot_frame, data, view):
    """
    Erzeugt einen Temperaturverlauf über die letzten 7 Tage als Seaborn-Lineplot.
    """
    if view.canvas:
        view.canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=data, x="Datum", y="Temperatur", ax=ax, color="tab:red")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))

    ax.set_title("Temperatur der letzten Woche")
    ax.set_ylabel("Temperatur (°C)")
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()

    view.canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    view.canvas.draw()
    view.canvas.get_tk_widget().pack(fill="both", expand=True)


def draw_analysis_plots(data, stats, target_frame):
    """
    Zeigt je ein Diagramm für Temperatur, Luftfeuchtigkeit und Luftdruck
    mit Min-, Max- und Durchschnittslinien für den gewählten Analysezeitraum.
    """
    for widget in target_frame.winfo_children():
        widget.destroy()

    metrics = ["Temperatur", "Luftfeuchtigkeit", "Luftdruck"]
    colors = ["tab:red", "tab:blue", "tab:green"]

    for metric, color in zip(metrics, colors):
        fig, ax = plt.subplots(figsize=(5, 2.5))
        sns.lineplot(data=data, x="Datum", y=metric, ax=ax, color=color)

        # Min, Max, Durchschnitt
        ax.axhline(stats[metric]["Min"], color=color, linestyle="--", label="Min")
        ax.axhline(stats[metric]["Max"], color=color, linestyle="--", label="Max")
        ax.axhline(stats[metric]["Durchschnitt"], color=color, linestyle="-", label="Ø")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))

        ax.set_title(f"{metric} im Zeitraum")
        ax.tick_params(axis='x', rotation=45)
        ax.legend(loc="center left", bbox_to_anchor=(1.05, 0.5), borderaxespad=0.5)
        fig.subplots_adjust(left=0.15, right=0.85, top=0.9, bottom=0.25)

        canvas = FigureCanvasTkAgg(fig, master=target_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=5)
