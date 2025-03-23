# Imports the main Tkinter window class and the GUI application logic from gui.py.
from tkinter import Tk
from gui import PennyPilotApp

# Entry point for the application.
# Initializes the Tkinter root window and launches the PennyPilotApp GUI.
if __name__ == "__main__":
    root = Tk()
    app = PennyPilotApp(root)
    root.mainloop()
