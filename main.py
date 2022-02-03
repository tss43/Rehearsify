# main.py
"""To treat directory as executable."""

import tkinter as tk

from src.GUI_interacting.RehearsifyGUI import RehearsifyGUI

# to enable executing module as script 
if __name__ == "__main__":
        
    root = tk.Tk()
    app = RehearsifyGUI(window=root) 
    root.mainloop() 
