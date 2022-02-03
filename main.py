# main.py
"""To treat directory as executable."""

from tkinter import Tk
from src.GUI_interacting.RehearsifyGUI import RehearsifyGUI

# to enable executing module as script 
if __name__ == "__main__":
        
    root = Tk()
    app = RehearsifyGUI(window=root) 
    app.window.mainloop() 
