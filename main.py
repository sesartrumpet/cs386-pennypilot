# Imports the main Tkinter window class and the GUI application logic from gui.py.
from tkinter import Tk
from gui import PennyPilotApp
from gui import show_login_window, show_main_app

# Entry point for the application.
# Initializes the Tkinter root window and launches the PennyPilotApp GUI.
if __name__ == "__main__":
    # Create the main window
    root = Tk()
    
    # initially hides main screen until login is verified
    root.withdraw()
    
     # Show the login screen; after login, load main app
    show_login_window(show_main_app, root)
    
    # Start the Tkinter event loop to keep the window open
    root.mainloop()
    
