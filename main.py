"""
Main entry point for the PennyPilot application.
This module initializes the application, sets up the database,
and manages the application's lifecycle from login to main window.
"""

# Import required modules
from tkinter import Tk, messagebox
from gui import PennyPilotApp
from gui import show_login_window, show_main_app
from database import initialize_database

def main():
    """
    Main entry point for the PennyPilot application.
    This function:
    1. Initializes the database
    2. Creates the main window
    3. Shows the login screen
    4. Starts the main application loop
    """
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
    
    # Initially hide main screen until login is verified
    root.withdraw()
    
    # Show the login screen; after login, load main app
    show_login_window(show_main_app, root)
    
    # Start the Tkinter event loop to keep the window open
    root.mainloop()

# Only run if this file is executed directly
if __name__ == "__main__":
    main()
    
