"""
Graphical User Interface module for the PennyPilot application.
This module handles all user interface components and interactions,
including the main application window, login screen, and trip planning interface.

The GUI is built using Tkinter and includes:
- Login/authentication system
- Trip selection and cost breakdown
- Savings calculation and display
- Date selection for trip planning
- Expense breakdown visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controllers import get_trips, calculate_savings_goal, handle_update_savings, fetch_trip_expense_breakdown
from database import get_user_savings
from tkcalendar import DateEntry 
import datetime
import threading
import mysql.connector
from controllers import handle_login

def set_window_size(window, width=400, height=600):
    """
    Centers and sets the size of a window on the screen.
    
    Args:
        window (tk.Tk or tk.Toplevel): The window to resize
        width (int): Desired width of the window
        height (int): Desired height of the window
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def setup_window_closing(window, root=None, cleanup_func=None):
    """
    Configures proper window closing behavior with cleanup.
    
    Args:
        window (tk.Tk or tk.Toplevel): The window to configure
        root (tk.Tk, optional): The root window to destroy
        cleanup_func (callable, optional): Function to call before closing
    """
    def on_closing():
        try:
            if cleanup_func:
                cleanup_func()
            if root:
                root.destroy()
            window.destroy()
        except tk.TclError:
            # Window was already destroyed, ignore the error
            pass
    
    window.protocol("WM_DELETE_WINDOW", on_closing)

def generate_future_dates():
    """
    Generates a list of dates for the next 30 days.
    Used for trip planning and date selection.
    
    Returns:
        list: List of datetime.date objects for the next 30 days
    """
    today = datetime.date.today()
    future_dates = []
    for i in range(1, 31):  
        future_dates.append(today + datetime.timedelta(days=i))
    return future_dates

class PennyPilotApp:
    """
    Main application class that manages the PennyPilot GUI.
    This class handles all user interface components and their interactions.
    
    Attributes:
        root (tk.Tk): The main application window
        connector (mysql.connector): Database connection object
        trips (list): List of available trips
        trip_var (tk.StringVar): Variable for selected trip
        calculation_ready (bool): Flag indicating if savings have been calculated
        last_calculated_data (dict): Stores the last successful calculation results
    """
    
    def __init__(self, root):
        """
        Initializes the PennyPilot application GUI.
        
        Args:
            root (tk.Tk): The main application window
        """
        self.root = root
        self.root.title("Penny Pilot - Trip Savings")
        self.connector = None  
        
        # Set window size
        set_window_size(root)
        
        # Set up window closing
        setup_window_closing(root, cleanup_func=self.on_closing)
        
        self.display_username()
        
        # Initialize trip selection
        self.trip_var = tk.StringVar()
        success, result = get_trips()
        if success:
            self.trips = result
        else:
            self.trips = []
            messagebox.showerror("Database Error", result)

        # Create trip selection dropdown
        self.trip_dropdown = ttk.Combobox(root, textvariable=self.trip_var, state="readonly", width=24)
        self.trip_dropdown["values"] = [f"{trip[0]} - ${trip[1]:.2f}" for trip in self.trips]
        self.trip_dropdown.pack(pady=5)
        
        # Bind selection event to update expense breakdown
        self.trip_dropdown.bind('<<ComboboxSelected>>', self.on_trip_selected)

        # Create savings input field with placeholder
        self.int_input = tk.Entry(root, fg='grey', width=24)
        self.int_input.insert(0, "Already Saved")
        self.int_input.pack(pady=5)

        # Set up placeholder behavior
        self.int_input.bind("<FocusIn>", self.clear_placeholder)
        self.int_input.bind("<FocusOut>", self.add_placeholder)

        # Create date selection widget
        self.create_date_dropdown()

        # Initialize calculation state
        self.calculation_ready = False
        self.last_calculated_data = {}

        # Create calculate button
        self.calc_btn = tk.Button(root, text="Calculate Savings Goal", command=self.calculate)
        self.calc_btn.pack(pady=5)

        # Create result display
        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)

        # Create savings breakdown table
        self.savings_table = ttk.Treeview(root, columns=("Period", "Amount"), show="headings", height=3)
        self.savings_table.heading("Period", text="Period")
        self.savings_table.heading("Amount", text="Amount")
        self.savings_table.pack(pady=10)

        # Initialize savings table with default values
        self.savings_table.insert("", "end", iid="month", values=("Monthly", "—"))
        self.savings_table.insert("", "end", iid="week", values=("Weekly", "—"))
        self.savings_table.insert("", "end", iid="day", values=("Daily", "—"))

        # Create expense breakdown table
        self.expense_breakdown_table = ttk.Treeview(root, columns=("Category", "Estimated Cost"), show="headings", height=7)
        self.expense_breakdown_table.heading("Category", text="Category")
        self.expense_breakdown_table.heading("Estimated Cost", text="Estimated Cost")
        self.expense_breakdown_table.pack(pady=10)

        # Initialize expense table with default values
        self.expense_breakdown_table.insert("", "end", iid="travelto", values=("Travel To", "—"))
        self.expense_breakdown_table.insert("", "end", iid="travelthere", values=("Travel There", "—"))
        self.expense_breakdown_table.insert("", "end", iid="food", values=("Food", "—"))
        self.expense_breakdown_table.insert("", "end", iid="housing", values=("Housing", "—"))
        self.expense_breakdown_table.insert("", "end", iid="school", values=("School", "—"))
        self.expense_breakdown_table.insert("", "end", iid="misc", values=("Misc", "—"))
        self.expense_breakdown_table.insert("", "end", iid="total", values=("Total", "—"))

        # Create confirm button
        self.confirm_btn = tk.Button(
            root,
            text="Confirm Trip Destination",
            command=self.handle_confirm_click
        )
        self.confirm_btn.pack(pady=10)
        self.confirm_btn.pack(ipadx=10)
        self.confirm_btn.pack(ipady=15)

    def display_username(self):
        """
        Displays a welcome message to the user.
        """
        greeting = tk.Label(self.root, text=f"Hello! Welcome to PennyPilot", font=("Arial", 14))
        greeting.pack(pady=10)
    
    def create_date_dropdown(self):
        """
        Creates a date selection widget using tkcalendar.
        """
        self.date_entry = DateEntry(
            self.root,
            width=21,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=datetime.datetime.now().year,
            month=datetime.datetime.now().month,
            day=datetime.datetime.now().day
        )
        self.date_entry.pack(pady=5)

    def calculate(self):
        """
        Initiates the savings calculation process.
        Validates input and starts calculation in a background thread.
        """
        selected = self.trip_var.get()
        if not selected:
            return
        username = selected.split(" - ")[0]  
        trip = next(t for t in self.trips if t[0] == username)

        # Get selected date
        date_str = self.date_entry.get_date().strftime("%Y-%m-%d")

        # Get and validate savings input
        saved_text = self.int_input.get()
        try:
            already_saved = int(saved_text) if saved_text != "Already Saved" else 0
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer for 'Already Saved'")
            return

        # Start calculation in background thread
        threading.Thread(target=self.calculate_in_background, args=(trip, date_str, already_saved)).start()

    def calculate_in_background(self, trip, date_str, already_saved):
        """
        Performs savings calculation in a background thread.
        Updates the UI with calculation results.
        
        Args:
            trip (tuple): Selected trip data (destination, cost)
            date_str (str): Selected departure date
            already_saved (float): Amount already saved
        """
        success, result = calculate_savings_goal(trip[1], date_str, already_saved)
        if success:
            self.result_label.config(text="")

            # Update savings table
            self.savings_table.item("month", values=("Monthly", f"${result['savings_per_month']}"))
            self.savings_table.item("week", values=("Weekly", f"${result['savings_per_week']}"))
            self.savings_table.item("day", values=("Daily", f"${result['savings_per_day']}"))

            self.update_expense_breakdown(trip[0])

        else:
            messagebox.showerror("Error", result)
        self.calculation_ready = True
        self.last_calculated_data = {
            "trip_name": trip[0],
            "total_cost": trip[1],
            "savings": result,
            "end_date": date_str
        }

        self.update_expense_breakdown(trip[0])

    def update_expense_breakdown(self, location):
        """
        Updates the expense breakdown table with data for the selected location.
        
        Args:
            location (str): The selected trip location
        """
        success, data = fetch_trip_expense_breakdown(location)
        print("DEBUG - raw_data:", data, "| type:", type(data))
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

    def on_closing(self):
        """
        Handles cleanup when the application window is closed.
        Closes database connections and performs other cleanup tasks.
        """
        if self.connector:
            try:
                self.connector.close()
                print("Database connection closed")
            except Exception as e:
                print(f"Error closing database connection: {e}")

    def create_connection(self):
        """
        Establishes a connection to the MySQL database.
        
        Returns:
            mysql.connector: Database connection object or None if connection fails
        """
        import config as myconfig
        config = myconfig.Config.dbinfo().copy()
        try:
            self.connector = mysql.connector.Connect(**config)
            return self.connector
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return None
    
    def clear_placeholder(self, event):
        """
        Clears the placeholder text when the input field is focused.
        
        Args:
            event: The focus event
        """
        if self.int_input.get() == "Already Saved":
            self.int_input.delete(0, tk.END)
            self.int_input.config(fg='black')

    def add_placeholder(self, event):
        """
        Restores the placeholder text if the input field is empty.
        
        Args:
            event: The focus event
        """
        if not self.int_input.get():
            self.int_input.insert(0, "Already Saved")
            self.int_input.config(fg='grey')
    
    def handle_confirm_click(self):
        """
        Handles the confirm button click event.
        Validates that calculations have been performed before proceeding.
        Updates the trip table with the selected trip information.
        """
        if not self.calculation_ready:
            messagebox.showerror("Error", "Please calculate trip savings before confirming.")
            return
            
        try:
            # Get the selected trip information
            selected = self.trip_var.get()
            if not selected:
                messagebox.showerror("Error", "No trip selected")
                return
                
            # Get the location from the trip destination
            # Format is "Location - $XXXX.XX", so split on " - " and take first part
            location = selected.split(" - ")[0]
            
            # Get the dates
            date_start = datetime.datetime.now().date()  # Today's date
            date_selected = self.date_entry.get_date()   # Date selected in the calendar
            
            # Connect to database
            conn = self.create_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to database")
                return
                
            cursor = conn.cursor()
            
            # First verify the location exists in tripDestination
            cursor.execute("SELECT location FROM tripDestination WHERE location = %s", (location,))
            if not cursor.fetchone():
                messagebox.showerror("Error", f"Invalid destination: {location}")
                return
            
            # Get current logged in username from userProfile
            cursor.execute("SELECT userName FROM userProfile LIMIT 1")
            user_result = cursor.fetchone()
            if not user_result:
                messagebox.showerror("Error", "No user profile found")
                return
                
            username = user_result[0]
            
            # First delete any existing trip for this user
            cursor.execute("DELETE FROM trip WHERE userName = %s", (username,))
            
            # Insert new trip information
            cursor.execute("""
                INSERT INTO trip (userName, location, dateStart, dateSelected)
                VALUES (%s, %s, %s, %s)
            """, (username, location, date_start, date_selected))
            
            conn.commit()
            
            # Print trip table contents for testing
            cursor.execute("SELECT * FROM trip")
            trips = cursor.fetchall()
            print("\nCurrent Trip Table Contents:")
            print("Username | Location | Start Date | Selected Date")
            print("-" * 50)
            for trip in trips:
                print(f"{trip[0]} | {trip[1]} | {trip[2]} | {trip[3]}")
            
            messagebox.showinfo("Success", "Trip destination confirmed successfully!")
            show_progress_window(self.last_calculated_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to confirm trip: {str(e)}")
        finally:
            if conn:
                conn.close()

    def on_trip_selected(self, event):
        """
        Handles the trip selection event.
        Updates the expense breakdown when a new trip is selected.
        
        Args:
            event: The selection event
        """
        selected = self.trip_var.get()
        if selected:
            location = selected.split(" - ")[0]
            self.update_expense_breakdown(location)

def show_main_app(root):
    """
    Initializes and displays the main application window.
    
    Args:
        root (tk.Tk): The root window
    """
    PennyPilotApp(root)

def show_login_window(start_main_app_callback, root):
    """
    Displays the login window and handles authentication.
    
    Args:
        start_main_app_callback (callable): Function to call after successful login
        root (tk.Tk): The root window
    """
    import tkinter as tk
    from tkinter import messagebox
    from controllers import handle_login

    # Create login window
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    
    # Set window size
    set_window_size(login_window)
    
    # Set up window closing
    setup_window_closing(login_window, root)
    
    # Create main frame
    main_frame = tk.Frame(login_window)
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Add title
    title_label = tk.Label(main_frame, text="PennyPilot", font=("Arial", 16, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Create login form
    login_frame = tk.Frame(main_frame)
    login_frame.pack(expand=True)
    
    # Username field
    username_entry = tk.Entry(login_frame, fg='grey')
    username_entry.insert(0, "Username")
    username_entry.grid(row=0, column=0, padx=10, pady=10)
    
    def clear_username_placeholder(event):
        if username_entry.get() == "Username":
            username_entry.delete(0, tk.END)
            username_entry.config(fg='black')
    
    def add_username_placeholder(event):
        if not username_entry.get():
            username_entry.insert(0, "Username")
            username_entry.config(fg='grey')
    
    username_entry.bind("<FocusIn>", clear_username_placeholder)
    username_entry.bind("<FocusOut>", add_username_placeholder)

    # Password field
    password_entry = tk.Entry(login_frame, fg='grey')
    password_entry.insert(0, "Password")
    password_entry.grid(row=1, column=0, padx=10, pady=10)
    
    def clear_password_placeholder(event):
        if password_entry.get() == "Password":
            password_entry.delete(0, tk.END)
            password_entry.config(fg='black', show='*')
    
    def add_password_placeholder(event):
        if not password_entry.get():
            password_entry.insert(0, "Password")
            password_entry.config(fg='grey', show='')
    
    password_entry.bind("<FocusIn>", clear_password_placeholder)
    password_entry.bind("<FocusOut>", add_password_placeholder)
    # Add Enter key binding to trigger login
    password_entry.bind("<Return>", lambda event: attempt_login())

    def attempt_login():
        """
        Attempts to authenticate the user with provided credentials.
        """
        username = username_entry.get() if username_entry.get() != "Username" else ""
        password = password_entry.get() if password_entry.get() != "Password" else ""
        if handle_login(username, password):
            login_window.destroy()
            root.deiconify()
            start_main_app_callback(root)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    # Login button
    login_button = tk.Button(main_frame, text="Login", command=attempt_login)
    login_button.pack(pady=10)
    
    # Create account button
    create_account_button = tk.Button(main_frame, text="Create Account", 
                                    command=lambda: show_create_account_window(login_window))
    create_account_button.pack(pady=10)

def show_create_account_window(login_window):
    """
    Displays the account creation window.
    
    Args:
        login_window (tk.Toplevel): The parent login window
    """
    import tkinter as tk
    from tkinter import messagebox
    from database import create_connection
    
    # Hide login window
    login_window.withdraw()
    
    # Create account window
    create_window = tk.Toplevel(login_window)
    create_window.title("Create Account")
    
    # Set window size
    set_window_size(create_window)
    
    def on_closing():
        create_window.destroy()
        login_window.deiconify()
    
    create_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Create main frame
    main_frame = tk.Frame(create_window)
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Add title
    title_label = tk.Label(main_frame, text="Create Account", font=("Arial", 16, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Create form
    form_frame = tk.Frame(main_frame)
    form_frame.pack(expand=True)
    
    # Username field
    username_label = tk.Label(form_frame, text="Username:", anchor='w')
    username_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
    username_entry = tk.Entry(form_frame)
    username_entry.grid(row=0, column=1, padx=10, pady=5)
    
    # Password field
    password_label = tk.Label(form_frame, text="Password:", anchor='w')
    password_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
    password_entry = tk.Entry(form_frame, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=5)
    
    # Confirm password field
    confirm_password_label = tk.Label(form_frame, text="Confirm Password:", anchor='w')
    confirm_password_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
    confirm_password_entry = tk.Entry(form_frame, show='*')
    confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)
    
    # First name field
    first_name_label = tk.Label(form_frame, text="First Name:", anchor='w')
    first_name_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
    first_name_entry = tk.Entry(form_frame)
    first_name_entry.grid(row=3, column=1, padx=10, pady=5)
    
    # Last name field
    last_name_label = tk.Label(form_frame, text="Last Name:", anchor='w')
    last_name_label.grid(row=4, column=0, padx=10, pady=5, sticky='w')
    last_name_entry = tk.Entry(form_frame)
    last_name_entry.grid(row=4, column=1, padx=10, pady=5)
    
    # Email field
    email_label = tk.Label(form_frame, text="NAU Email:", anchor='w')
    email_label.grid(row=5, column=0, padx=10, pady=5, sticky='w')
    email_entry = tk.Entry(form_frame)
    email_entry.grid(row=5, column=1, padx=10, pady=5)
    
    def create_account():
        """
        Attempts to create a new user account with provided information.
        Validates input and handles database operations.
        """
        # Get input values
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        
        # Validate required fields
        if not all([username, password, confirm_password, first_name, last_name, email]):
            messagebox.showerror("Error", "All fields are required")
            return
            
        # Validate password match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        # Validate email format
        if '@nau.edu' not in email:
            messagebox.showerror("Error", "Please use a valid NAU email address")
            return
            
        try:
            # Connect to database
            conn = create_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to database")
                return
                
            cursor = conn.cursor()
            
            # Check for existing username
            cursor.execute("SELECT * FROM userProfile WHERE userName = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return
                
            # Check for existing email
            cursor.execute("SELECT * FROM userProfile WHERE nauEmail = %s", (email,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Email address already registered")
                return
                
            # Create new user
            cursor.execute("""
                INSERT INTO userProfile (userName, passwordHash, firstName, lastName, nauEmail)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, password, first_name, last_name, email))
            
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            create_window.destroy()
            login_window.deiconify()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    # Create account button
    create_button = tk.Button(main_frame, text="Create Account", command=create_account)
    create_button.pack(pady=10)
    
    # Back to Login button
    back_button = tk.Button(main_frame, text="Back to Login", 
                          command=lambda: [create_window.destroy(), login_window.deiconify()])
    back_button.pack(pady=10)

def show_progress_window(data):
    """
    Displays a window showing the progress of the selected trip.
    
    Args:
        data (dict): Trip data including name, cost, savings, and end date
    """
    import tkinter as tk
    from tkinter import ttk
    from database import create_connection

    progress_window = tk.Toplevel()
    progress_window.title("Trip Progress")
    set_window_size(progress_window, width=350, height=250)

    progress_window.grab_set()

    def change_destination():
        """
        Handles the change destination button click.
        Deletes the current trip data and closes the progress window.
        """
        try:
            # Connect to database
            conn = create_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to database")
                return
                
            cursor = conn.cursor()
            
            # Get current logged in username from userProfile
            cursor.execute("SELECT userName FROM userProfile LIMIT 1")
            user_result = cursor.fetchone()
            if user_result:
                username = user_result[0]
                # Delete the trip for this user
                cursor.execute("DELETE FROM trip WHERE userName = %s", (username,))
                conn.commit()
                print(f"Deleted trip data for user: {username}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete trip data: {str(e)}")
        finally:
            if conn:
                conn.close()
            progress_window.destroy()

    # Code to show trip details goes here
    #
    #
    #
    #

    close_button = tk.Button(progress_window, text="Change Destination", command=change_destination)
    close_button.pack(pady=20)

    setup_window_closing(progress_window)