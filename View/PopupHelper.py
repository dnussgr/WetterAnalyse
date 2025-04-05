import tkinter as tk
from tkcalendar import DateEntry

def force_popup_above(entry: DateEntry):
    """
    Erzwingt, dass sich das Kalender-Popup immer oberhalb des DateEntry-Feldes öffnet.
    """

    def reposition_popup(_event=None):
        top = getattr(entry, "_top_cal", None)
        if isinstance(top, tk.Toplevel):
            top.update_idletasks()
            x = entry.winfo_rootx()
            y = entry.winfo_rooty()
            h = top.winfo_height()
            top.geometry(f"+{x}+{y - h - 2}")

    def bind_on_open(*_):
        top = getattr(entry, "_top_cal", None)
        if isinstance(top, tk.Toplevel):
            top.bind("<Map>", reposition_popup)

    entry.bind("<Button-1>", bind_on_open, add="+")
