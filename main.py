# Imports the main Tkinter window class and the GUI application logic from gui.py.
from tkinter import Tk, messagebox
from gui import PennyPilotApp
from gui import show_login_window, show_main_app
from database import initialize_database

# Entry point for the application.
# Initializes the Tkinter root window and launches the PennyPilotApp GUI.
if __name__ == "__main__":
    # Initialize the database
    if not initialize_database():
        messagebox.showerror("Database Error", 
            "Failed to initialize database. Please ensure:\n"
            "1. MySQL server is running\n"
            "2. Your credentials in config.py are correct\n"
            "3. You have proper permissions to create databases")
        exit(1)
    
    # Create the main window
    root = Tk()
    
    # initially hides main screen until login is verified
    root.withdraw()
    
    # Show the login screen; after login, load main app
    show_login_window(show_main_app, root)
    
    # Start the Tkinter event loop to keep the window open
    root.mainloop()
    
