# main.py
"""To treat directory as executable."""

from src.GUI_interacting.RehearsifyGUI import RehearsifyGUI

# to enable executing module as script 
if __name__ == "__main__":
        
    app = RehearsifyGUI() 
    app.window.mainloop() 
