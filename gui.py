import tkinter as tk
from tkinter import ttk, messagebox
from controllers import get_trips, calculate_savings_goal, handle_update_savings, fetch_trip_expense_breakdown
from database import get_user_savings
from tkcalendar import DateEntry 
import datetime
import threading
import mysql.connector


# Generates a list of 30 dates starting from today to be used for travel planning.
def generate_future_dates():
    today = datetime.date.today()
    future_dates = []
    for i in range(1, 31):  
        future_dates.append(today + datetime.timedelta(days=i))
    return future_dates

# Main application class that defines and manages the entire Penny Pilot trip savings GUI.
class PennyPilotApp:
    
    # Initializes the GUI layout, connects to the database, and sets up all UI components.
    def __init__(self, root):
        self.root = root
        self.root.title("Penny Pilot - Trip Savings")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.connector = None  
        
        self.display_username()
        
        self.trip_var = tk.StringVar()
        success, result = get_trips()
        if success:
            self.trips = result
        else:
            self.trips = []
            messagebox.showerror("Database Error", result)

        self.trip_dropdown = ttk.Combobox(root, textvariable=self.trip_var, state="readonly")
        self.trip_dropdown["values"] = [f"{trip[0]} - ${trip[1]:.2f}" for trip in self.trips]
        self.trip_dropdown.pack(pady=5)

        # Date input with calendar widget
        self.create_date_dropdown()

        # Calculate button
        self.calc_btn = tk.Button(root, text="Calculate Savings Goal", command=self.calculate)
        self.calc_btn.pack(pady=5)

        # Result
        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)

        # Create a savings breakdown table
        self.savings_table = ttk.Treeview(root, columns=("Period", "Amount"), show="headings", height=3)
        self.savings_table.heading("Period", text="Period")
        self.savings_table.heading("Amount", text="Amount")
        self.savings_table.pack(pady=10)

        # Insert default rows
        self.savings_table.insert("", "end", iid="month", values=("Monthly", "—"))
        self.savings_table.insert("", "end", iid="week", values=("Weekly", "—"))
        self.savings_table.insert("", "end", iid="day", values=("Daily", "—"))

        self.expense_breakdown_table = ttk.Treeview(root, columns=("Category", "Estimated Cost"), show="headings", height=7)
        self.expense_breakdown_table.heading("Category", text="Category")
        self.expense_breakdown_table.heading("Estimated Cost", text="Estimated Cost")
        self.expense_breakdown_table.pack(pady=10)

        # Insert default rows with em dashes and unique IDs
        self.expense_breakdown_table.insert("", "end", iid="travelto", values=("Travel To", "—"))
        self.expense_breakdown_table.insert("", "end", iid="travelthere", values=("Travel There", "—"))
        self.expense_breakdown_table.insert("", "end", iid="food", values=("Food", "—"))
        self.expense_breakdown_table.insert("", "end", iid="housing", values=("Housing", "—"))
        self.expense_breakdown_table.insert("", "end", iid="school", values=("School", "—"))
        self.expense_breakdown_table.insert("", "end", iid="misc", values=("Misc", "—"))
        self.expense_breakdown_table.insert("", "end", iid="total", values=("Total", "—"))
    
    # Displays a welcome greeting to the user.
    def display_username(self):
        greeting = tk.Label(self.root, text=f"Hello! Welcome to PennyPilot", font=("Arial", 14))
        greeting.pack(pady=10) # Add label to window
    
    # Adds a date picker widget for selecting the trip end date.
    def create_date_dropdown(self):
        
        # Create DateEntry widget from tkcalendar
        self.date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2, year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        self.date_entry.pack(pady=5)

    # Starts a background thread to calculate savings based on trip and date input.
    def calculate(self):
        selected = self.trip_var.get()
        if not selected:
            return
        username = selected.split(" - ")[0]  
        trip = next(t for t in self.trips if t[0] == username)

        # Get the selected date from the calendar widget
        date_str = self.date_entry.get_date().strftime("%Y-%m-%d")

        # Run calculation and graph drawing in a separate thread
        threading.Thread(target=self.calculate_in_background, args=(trip, date_str)).start()

    # Runs the savings calculation and updates UI tables in a background thread.
    def calculate_in_background(self, trip, date_str):
        success, result = calculate_savings_goal(trip[1], date_str)
        if success:
            self.result_label.config(text="")

            self.savings_table.item("month", values=("Monthly", f"${result['savings_per_month']}"))
            self.savings_table.item("week", values=("Weekly", f"${result['savings_per_week']}"))
            self.savings_table.item("day", values=("Daily", f"${result['savings_per_day']}"))

            self.update_expense_breakdown(trip[0])

        else:
            messagebox.showerror("Error", result)

    # Fetches and displays a detailed cost breakdown for a trip by category.
    def update_expense_breakdown(self, location):
        success, data = fetch_trip_expense_breakdown(location)
        categories = ["Travel To", "Travel There", "Food", "Housing", "School", "Misc"]

        if success and data:
            total = 0
            for cat, val in zip(categories, data):
                self.expense_breakdown_table.item(cat.lower().replace(" ", ""), values=(cat, f"${val:,.2f}"))
                total += val
            self.expense_breakdown_table.item("total", values=("Total", f"${total:,.2f}"))
        else:
            for cat in categories:
                self.expense_breakdown_table.item(cat.lower().replace(" ", ""), values=(cat, "—"))
            self.expense_breakdown_table.item("total", values=("Total", "—"))

    # Closes the database connection (if active) and gracefully exits the application.
    def on_closing(self):
        """Handle cleanup when window is closed"""
        if self.connector:
            try:
                self.connector.close()
                print("Database connection closed")
            except Exception as e:
                print(f"Error closing database connection: {e}")
        self.root.destroy()

    # Establishes a connection to the MySQL database if not already connected.
    def create_connection(self):
        """Create database connection if needed"""
        if not self.connector or not self.connector.is_connected():
            import config as myconfig
            config = myconfig.Config.dbinfo().copy()
            try:
                self.connector = mysql.connector.Connect(**config)
            except mysql.connector.Error as err:
                print(f"Error connecting to database: {err}")
                return None
        return self.connector
    
    
    