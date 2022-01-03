# main.py
"""To treat directory as executable."""

import tkinter as tk

from src.GUI_interacting.RehearsifyGUI import RehearsifyGUI

def open_Rehearsify_GUI():
    """ Open the main Rehearsify GUI window. """
    root = tk.Tk()
    app = RehearsifyGUI(window=root) 
    root.mainloop()


# to enable executing module as script 
if __name__ == "__main__":
    open_Rehearsify_GUI()

