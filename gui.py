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
#new
import os
from PIL import Image, ImageTk
from controllers import get_trips, calculate_savings_goal, handle_update_savings, fetch_trip_expense_breakdown
from database import get_user_savings, create_connection
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

    #new
    def back_to_login(self):
        """
        Returns the user to the login screen.
        """
        self.root.withdraw()  # Hide main window
        from gui import show_login_window
        show_login_window(show_main_app, self.root)


    def __init__(self, root, username):
        """
        Initializes the PennyPilot application GUI.
        
        Args:
            root (tk.Tk): The main application window
        """
        self.root = root
        self.savings_result = {}
        self.username = username
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
        
        # Create temporary message label (initially empty)
        self.temp_message_label = tk.Label(root, text="", fg="green", font=("Arial", 10))
        self.temp_message_label.pack(pady=2)

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
            text="Confirm Trip Destination",bg="green", fg="white", activebackground="darkgreen",
            command=self.handle_confirm_click
        )
        self.confirm_btn.pack(pady=10)
        self.confirm_btn.pack(ipadx=10)
        self.confirm_btn.pack(ipady=15)

        #new
        # Back to login button
        self.back_btn = tk.Button(self.root, text="Back to Login", command=self.back_to_login, bg="green", fg="white", activebackground="darkgreen")
        self.back_btn.pack(pady=10)


    def display_username(self):
        """
        Displays a welcome message to the user.
        """
        user = self.username
        greeting = tk.Label(self.root, text=f"Hello {user}! Welcome to PennyPilot", font=("Arial", 14))
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

        # Show temporary message
        self.show_temporary_message("Updated Goal")
        
        # Start calculation in background thread
        threading.Thread(target=self.calculate_in_background, args=(trip, date_str, already_saved)).start()

    def calculate_in_background(self, trip, date_str, already_saved):
        """
        Performs savings calculation in a background thread.
        Updates the UI with calculation results.
        
        Args:
            trip (tuple): Selected trip data (destination, cost)
            date_str (str): Selected departure date
            already_saved (int): Amount already saved
        """
        success, result = calculate_savings_goal(trip[1], date_str, already_saved)
        if success:
            self.result_label.config(text="")

            # Update savings table
            self.savings_table.item("month", values=("Monthly", f"${result['savings_per_month']}"))
            self.savings_table.item("week", values=("Weekly", f"${result['savings_per_week']}"))
            self.savings_table.item("day", values=("Daily", f"${result['savings_per_day']}"))

            self.savings_result = result
            
            self.update_expense_breakdown(trip[0])

        else:
            messagebox.showerror("Error", result)
        self.calculation_ready = True
        self.last_calculated_data = {
            "trip_name": trip[0],
            "total_cost": trip[1],
            "savings": result,
            "end_date": date_str,
            "progress": round(min((already_saved / trip[1]) * 100, 100), 2)
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
        current_value = self.int_input.get()
        # Only restore placeholder if the field is empty or contains "Already Saved"
        if not current_value or current_value == "Already Saved":
            self.int_input.insert(0, "Already Saved")
            self.int_input.config(fg='grey')
    
    def handle_confirm_click(self):
        if not self.calculation_ready:
            messagebox.showerror("Error", "Please calculate trip savings before confirming.")
            return

        selected = self.trip_var.get()
        if not selected:
            messagebox.showerror("Error", "No trip selected")
            return

        location = selected.split(" - ")[0]
        
        # Get money saved
        saved_text = self.int_input.get()
        try:
            money_saved = int(saved_text) if saved_text != "Already Saved" else 0
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for money saved")
            return

        try:
            conn = self.create_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to database")
                return

            cursor = conn.cursor()
            
            cursor.execute("SELECT location FROM tripDestination WHERE location = %s", (location,))
            if not cursor.fetchone():
                messagebox.showerror("Error", f"Invalid destination: {location}")
                return

            cursor.execute("DELETE FROM trip WHERE userName = %s", (self.username,))
            
            date_start = datetime.datetime.now().date()
            date_selected = self.date_entry.get_date()
            cursor.execute("""
                INSERT INTO trip (userName, location, dateStart, dateSelected, moneySaved)
                VALUES (%s, %s, %s, %s, %s)
            """, (self.username, location, date_start, date_selected, money_saved))
            conn.commit()

            cursor.execute("""
                SELECT 
                t.location, 
                td.university, 
                t.dateStart, 
                t.dateSelected,
                t.moneySaved,
                p.Travelto, 
                p.Travelthere, 
                p.Food, 
                p.Housing, 
                p.School, 
                p.Misc
                FROM trip t
                JOIN tripDestination td ON t.location = td.location
                JOIN prices p ON t.location = p.location
                WHERE t.userName = %s
            """, (self.username,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "No trip data found for user.")
                return

            trip_data = {
                "trip_name": row[0],
                "university": row[1],
                "date_start": row[2],
                "date_selected": row[3],
                "money_saved": row[4],
                "prices": {
                    "Travelto": row[5],
                    "Travelthere": row[6],
                    "Food": row[7],
                    "Housing": row[8],
                    "School": row[9],
                    "Misc": row[10]
                },
                "savings": self.savings_result,
                "progress": self.last_calculated_data.get("progress", 0)
            }

            trip_data["main_window"] = self.root

            show_progress_window(trip_data)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to confirm trip: {str(e)}")
        finally:
            if conn:
                conn.close()

    def show_temporary_message(self, message):
        """
        Shows a temporary message that disappears after 3 seconds.
        
        Args:
            message (str): The message to display
        """
        # Update the label with the message
        self.temp_message_label.config(text=message)
        
        # Schedule the message to disappear after 3 seconds
        self.root.after(3000, self.clear_temporary_message)
        
    def clear_temporary_message(self):
        """
        Clears the temporary message.
        """
        self.temp_message_label.config(text="")

def show_main_app(root, username):
    """
    Initializes and displays the main application window.
    
    Args:
        root (tk.Tk): The root window
        username (str): The logged in user's username
    """
    # Check if user has existing trip and get saved amount
    try:
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT moneySaved FROM trip WHERE userName = %s", (username,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            app = PennyPilotApp(root, username)
            
            # If there's an existing saved amount, populate it
            if result and result[0] is not None:
                app.int_input.delete(0, tk.END)
                app.int_input.insert(0, str(result[0]))
                app.int_input.config(fg='black')
    except Exception as e:
        print(f"Error fetching saved amount: {e}")
        app = PennyPilotApp(root, username)

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
    from database import create_connection
    import datetime

    # Create login window
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    #new
    login_window.configure(bg="#f5f5f5")
    
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

    def attempt_login():
        """
        Attempts to authenticate the user with provided credentials.
        """
        username = username_entry.get() if username_entry.get() != "Username" else ""
        password = password_entry.get() if password_entry.get() != "Password" else ""
        if handle_login(username, password):
            # Check if user has an existing trip
            try:
                conn = create_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT 
                        t.location, 
                        td.university, 
                        t.dateStart, 
                        t.dateSelected,
                        t.moneySaved,
                        p.Travelto, 
                        p.Travelthere, 
                        p.Food, 
                        p.Housing, 
                        p.School, 
                        p.Misc
                        FROM trip t
                        JOIN tripDestination td ON t.location = td.location
                        JOIN prices p ON t.location = p.location
                        WHERE t.userName = %s
                    """, (username,))
                    
                    trip_data = cursor.fetchone()
                    cursor.close()
                    conn.close()
                    
                    if trip_data:
                        # Calculate total cost
                        total_cost = sum([trip_data[5], trip_data[6], trip_data[7], 
                                        trip_data[8], trip_data[9], trip_data[10]])
                        
                        # Calculate daily savings based on remaining time and money
                        days_remaining = (trip_data[3] - datetime.datetime.now().date()).days
                        money_saved = trip_data[4]
                        remaining_amount = max(0, total_cost - money_saved)  # Ensure non-negative
                        
                        if days_remaining > 0:
                            daily_amount = min(remaining_amount / days_remaining, remaining_amount)  # Cap at remaining amount
                            savings_info = {
                                "savings_per_day": daily_amount,
                                "savings_per_week": min(daily_amount * 7, remaining_amount),
                                "savings_per_month": min(daily_amount * 30, remaining_amount)
                            }
                        else:
                            # If past the target date, set all values to remaining amount
                            savings_info = {
                                "savings_per_day": remaining_amount,
                                "savings_per_week": remaining_amount,
                                "savings_per_month": remaining_amount
                            }
                        
                        # User has an existing trip, prepare data for progress window
                        trip_info = {
                            "trip_name": trip_data[0],
                            "university": trip_data[1],
                            "date_start": trip_data[2],
                            "date_selected": trip_data[3],
                            "money_saved": trip_data[4],
                            "prices": {
                                "Travelto": trip_data[5],
                                "Travelthere": trip_data[6],
                                "Food": trip_data[7],
                                "Housing": trip_data[8],
                                "School": trip_data[9],
                                "Misc": trip_data[10]
                            },
                            "savings": savings_info,
                            "progress": round(min((trip_data[4] / total_cost) * 100, 100), 2),
                            "main_window": root,
                            "userName": username  # Add username to trip data
                        }
                        
                        login_window.destroy()
                        show_progress_window(trip_info)
                        return
                    
                # If no trip found or error occurred, proceed to main app
                login_window.destroy()
                root.deiconify()
                start_main_app_callback(root, username)
                
            except Exception as e:
                print(f"Error checking for existing trip: {e}")
                # If there's an error, fall back to main app
                login_window.destroy()
                root.deiconify()
                start_main_app_callback(root, username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    # Add Enter key binding to trigger login
    password_entry.bind("<Return>", lambda event: attempt_login())
    
    # Login button
    #new
    login_button = tk.Button(main_frame, text="Login", command=attempt_login, bg="green", fg="white", activebackground="darkgreen")
    login_button.pack(pady=10)
    
    # Create Account button
    #new
    create_account_button = tk.Button(main_frame, text="Create Account", bg="green", fg="white", activebackground="darkgreen",
                                    command=lambda: show_create_account_window(login_window))
    create_account_button.pack(pady=10)

    #new
    # Add images to the login window
    try:
        base_dir = os.path.dirname(__file__)
        image_dir = os.path.join(base_dir, "images")

        earth_img_path = os.path.join(image_dir, "earth.png")
        student_img_path = os.path.join(image_dir, "student.png")

        earth_img = Image.open(earth_img_path).convert("RGBA").resize((95, 95), Image.Resampling.LANCZOS)
        student_img = Image.open(student_img_path).convert("RGBA").resize((100, 250), Image.Resampling.LANCZOS)

        earth_photo = ImageTk.PhotoImage(earth_img)
        student_photo = ImageTk.PhotoImage(student_img)

        earth_label = tk.Label(login_window, image=earth_photo, borderwidth=0, highlightthickness=0)
        earth_label.image = earth_photo
        earth_label.place(x=10, y=10)

        student_label = tk.Label(login_window, image=student_photo,borderwidth=0, highlightthickness=0)
        student_label.image = student_photo
        student_label.place(relx=1.0, rely=1.0, anchor="se", x=-5, y=-5)

    except Exception as e:
        print("Image display error:", e)


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
    back_button = tk.Button(main_frame, text="Back to Login", bg="green", fg="white", activebackground="darkgreen", 
                          command=lambda: [create_window.destroy(), login_window.deiconify()])
    back_button.pack(pady=10)

def show_progress_window(data):
    """
    Displays a window showing the progress of the selected trip with
    information pulled from the database. This window includes:
    - Real-time savings updates
    - Progress tracking
    - Savings goals calculation
    - Visual feedback through progress bar
    
    Args:
        data (dict): Trip data including:
            - trip_name (str): Name of the destination
            - university (str): Associated university
            - date_start (datetime): Trip start date
            - date_selected (datetime): Selected future date
            - money_saved (float): Current savings amount
            - prices (dict): Breakdown of trip costs
            - savings (dict): Savings goals per period
            - userName (str): Current user's username
    """
    import tkinter as tk
    from tkinter import ttk, messagebox
    import datetime
    from controllers import handle_update_savings, calculate_savings_goal

    # Hide main window while showing progress
    main_window = data.get('main_window')
    if main_window:
        main_window.withdraw()

    # Create and configure progress window
    progress_window = tk.Toplevel()
    progress_window.title("Trip Progress")
    set_window_size(progress_window, width=450, height=600)
    progress_window.grab_set()  # Make window modal

    # Create main frame for better organization and padding
    main_frame = tk.Frame(progress_window)
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)

    # Display trip destination and university headers
    tripHeader = tk.Label(
        main_frame,
        text=f"{data['trip_name']}",
        font=("Arial", 16, "bold"),
        pady=10
    )
    tripHeader.pack()

    uniHeader = tk.Label(
        main_frame,
        text=f"{data['university']}",
        font=("Arial", 12, "bold"),
        pady=10
    )
    uniHeader.pack()

    # Calculate initial savings and total cost
    original_saved = data.get('money_saved', 0)
    start_date = data.get('date_start')
    daily_savings = data.get('savings', {}).get('savings_per_day', 0)
    total_cost = sum(data.get('prices', {}).values())
    
    # Calculate accumulated savings based on time passed
    if isinstance(start_date, datetime.date):
        days_passed = (datetime.datetime.now().date() - start_date).days
        remaining_cost = max(0, total_cost - original_saved)
        if days_passed > 0:
            accumulated_savings = min(daily_savings * days_passed, remaining_cost)  # Cap at remaining cost
            total_saved = min(original_saved + accumulated_savings, total_cost)  # Cap at total cost
        else:
            total_saved = original_saved
    else:
        total_saved = original_saved

    # Create frame for savings update controls
    update_frame = tk.Frame(main_frame)
    update_frame.pack(pady=10)

    # Create entry widget for new savings amount
    savings_var = tk.StringVar(value=str(total_saved))
    savings_entry = tk.Entry(update_frame, textvariable=savings_var, width=15)
    savings_entry.pack(side=tk.LEFT, padx=5)

    # Add status message label for feedback
    status_label = tk.Label(
        main_frame,
        text="",
        font=("Arial", 10),
        fg="green"  # Default to green for success messages
    )
    status_label.pack(pady=5)

    def clear_status():
        """Clears the status message after a delay."""
        status_label.config(text="")

    def update_savings_display():
        """
        Handles the savings update process:
        1. Validates the new savings amount
        2. Updates the database
        3. Recalculates all derived values
        4. Updates the UI in real-time
        5. Provides visual feedback
        """
        try:
            # Input validation
            new_savings = float(savings_var.get())
            if new_savings < 0:
                status_label.config(text="Error: Savings amount cannot be negative", fg="red")
                main_frame.after(3000, clear_status)
                return
            
            # Update database with new savings amount
            success, message = handle_update_savings(new_savings, data.get('userName'))
            if success:
                # Convert values to float for calculations
                total_cost_float = float(total_cost)
                new_savings_float = float(new_savings)
                
                # Update savings display
                savings_label.config(text=f"Current Savings: ${new_savings_float:,.2f}")
                
                # Update remaining amount
                remaining = max(0, total_cost_float - new_savings_float)
                remaining_label.config(text=f"Remaining Amount: ${remaining:,.2f}")
                
                # Update progress visualization
                new_progress = min(100, (new_savings_float / total_cost_float) * 100) if total_cost_float > 0 else 0
                progress_bar["value"] = new_progress
                progress_label.config(text=f"{new_progress:.1f}%")
                
                # Force immediate update of progress bar
                progress_bar.update()
                progress_bar.update_idletasks()
                
                # Recalculate savings goals with new amount
                success, new_goals = calculate_savings_goal(
                    total_cost_float, 
                    data['date_selected'].strftime("%Y-%m-%d"), 
                    new_savings_float
                )
                
                if success:
                    # Update savings goals table
                    for item in savings_table.get_children():
                        savings_table.delete(item)
                    
                    # Insert new calculated goals
                    savings_table.insert("", "end", values=("Monthly", fmt(new_goals.get("savings_per_month"))))
                    savings_table.insert("", "end", values=("Weekly", fmt(new_goals.get("savings_per_week"))))
                    savings_table.insert("", "end", values=("Daily", fmt(new_goals.get("savings_per_day"))))
                    
                    # Force immediate update of table
                    savings_table.update()
                    savings_table.update_idletasks()
                
                # Update stored data
                data['money_saved'] = new_savings_float
                nonlocal total_saved
                total_saved = new_savings_float
                
                # Force immediate update of all UI elements
                savings_label.update()
                remaining_label.update()
                progress_label.update()
                cost_label.update()
                
                # Force update of containers
                main_frame.update()
                main_frame.update_idletasks()
                progress_window.update()
                progress_window.update_idletasks()
                
                # Show success message with auto-clear
                status_label.config(text="✓ Savings updated successfully!", fg="green")
                main_frame.after(3000, clear_status)
            else:
                # Show error message with auto-clear
                status_label.config(text=f"Error: {message}", fg="red")
                main_frame.after(3000, clear_status)
        except ValueError:
            # Show input validation error with auto-clear
            status_label.config(text="Error: Please enter a valid number", fg="red")
            main_frame.after(3000, clear_status)

    # Create update button
    update_button = tk.Button(update_frame, text="Update Savings", command=update_savings_display)
    update_button.pack(side=tk.LEFT, padx=5)

    # Display financial information labels
    savings_label = tk.Label(
        main_frame,
        text=f"Current Savings: ${total_saved:,.2f}",
        font=("Arial", 12),
        pady=5
    )
    savings_label.pack()

    remaining = max(0, total_cost - total_saved)
    remaining_label = tk.Label(
        main_frame,
        text=f"Remaining Amount: ${remaining:,.2f}",
        font=("Arial", 12),
        pady=5
    )
    remaining_label.pack()

    cost_label = tk.Label(
        main_frame,
        text=f"Total Trip Cost: ${total_cost:,.2f}",
        font=("Arial", 12),
        pady=5
    )
    cost_label.pack()

    # Calculate and display progress percentage
    if total_cost > 0:
        progress = min(100, (total_saved / total_cost) * 100)
    else:
        progress = 0

    # Create progress bar section
    tk.Label(main_frame, text="Trip Progress", font=("Arial", 10, "bold")).pack(pady=(10, 0))
    progress_bar = ttk.Progressbar(main_frame, mode="determinate", length=300)
    progress_bar["value"] = progress
    progress_bar.pack(pady=5)

    progress_label = tk.Label(
        main_frame,
        text=f"{progress:.1f}%",
        font=("Arial", 10)
    )
    progress_label.pack()

    # Create savings goals section
    tk.Label(main_frame, text="Savings Goals", font=("Arial", 10, "bold")).pack(pady=(15, 5))
    savings_frame = tk.Frame(main_frame)
    savings_frame.pack(pady=5)

    # Create savings breakdown table
    savings_table = ttk.Treeview(savings_frame, columns=("Period", "Amount"), show="headings", height=3)
    savings_table.heading("Period", text="Period")
    savings_table.heading("Amount", text="Amount")
    savings_table.column("Period", anchor="center", width=100)
    savings_table.column("Amount", anchor="center", width=150)
    savings_table.pack()

    def fmt(val):
        """Formats monetary values with dollar sign and two decimal places."""
        return f"${float(val):,.2f}" if val is not None else "—"

    # Calculate and display initial savings goals
    success, goals = calculate_savings_goal(total_cost, data['date_selected'].strftime("%Y-%m-%d"), total_saved)
    if success:
        savings_table.insert("", "end", values=("Monthly", fmt(goals.get("savings_per_month"))))
        savings_table.insert("", "end", values=("Weekly", fmt(goals.get("savings_per_week"))))
        savings_table.insert("", "end", values=("Daily", fmt(goals.get("savings_per_day"))))
    else:
        savings_table.insert("", "end", values=("Monthly", "—"))
        savings_table.insert("", "end", values=("Weekly", "—"))
        savings_table.insert("", "end", values=("Daily", "—"))

    def on_change_destination():
        """
        Handles the change destination button click.
        Returns to main window and transfers current savings amount.
        """
        if main_window:
            main_window.deiconify()
            
            # Create the app instance
            app = PennyPilotApp(main_window, data.get('userName'))
            
            # Get the current money saved value from the data dictionary
            money_saved = data.get('money_saved', 0)
            print(f"DEBUG: Setting money saved to {money_saved}")
            
            # Temporarily unbind the placeholder event handlers
            app.int_input.unbind("<FocusIn>")
            app.int_input.unbind("<FocusOut>")
            
            # Clear the placeholder text and set the actual value
            app.int_input.delete(0, tk.END)
            app.int_input.insert(0, str(int(money_saved)))
            app.int_input.config(fg='black')
            
            # Rebind the placeholder event handlers
            app.int_input.bind("<FocusIn>", app.clear_placeholder)
            app.int_input.bind("<FocusOut>", app.add_placeholder)
            
            # Force update the UI
            app.int_input.update()
            
            # Close the progress window
            progress_window.destroy()

    # Add change destination button
    tk.Button(main_frame, text="Change Destination", command=on_change_destination).pack(pady=15)

    def on_closing():
        """Handles window closing by destroying all windows."""
        if main_window:
            main_window.destroy()
        progress_window.destroy()

    # Set up window closing behavior
    progress_window.protocol("WM_DELETE_WINDOW", on_closing)
