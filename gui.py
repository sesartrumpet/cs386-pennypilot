# GUI file for PennyPilot: defines the app's layout and interactions
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
    """Sets the window size and centers it on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def setup_window_closing(window, root=None, cleanup_func=None):
    """
    Sets up window closing behavior for any window in the application.
    Args:
        window: The window to set up closing for
        root: The root window to destroy (if any)
        cleanup_func: Optional function to call before closing (e.g., for database cleanup)
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

# Generates a list of 30 dates starting from today to be used for travel planning.
def generate_future_dates():
    today = datetime.date.today()
    future_dates = []
    for i in range(1, 31):  
        future_dates.append(today + datetime.timedelta(days=i))
    return future_dates


# Main application class that defines and manages the entire Penny Pilot trip savings GUI.
class PennyPilotApp:
    
    # Constructor: Builds and displays the GUI layout
    def __init__(self, root):
        self.root = root
        self.root.title("Penny Pilot - Trip Savings")
        self.connector = None  
        
        # Set window size
        set_window_size(root)
        
        # Set up window closing
        setup_window_closing(root, cleanup_func=self.on_closing)
        
        self.display_username()
        
        self.trip_var = tk.StringVar()
        success, result = get_trips()
        if success:
            self.trips = result
        else:
            self.trips = []
            messagebox.showerror("Database Error", result)

        # Dropdown to select a trip (e.g., "Rome - $2100.00")
        self.trip_dropdown = ttk.Combobox(root, textvariable=self.trip_var, state="readonly", width=24)
        self.trip_dropdown["values"] = [f"{trip[0]} - ${trip[1]:.2f}" for trip in self.trips]
        self.trip_dropdown.pack(pady=5)

         # Input for money already saved with placeholder
        self.int_input = tk.Entry(root, fg='grey', width=24)
        self.int_input.insert(0, "Already Saved")
        self.int_input.pack(pady=5)

        # Bind focus events to simulate placeholder behavior
        self.int_input.bind("<FocusIn>", self.clear_placeholder)
        self.int_input.bind("<FocusOut>", self.add_placeholder)

        # Date input with calendar widget
        self.create_date_dropdown()

        # Bool to store if calculate button has generated trip data
        self.calculation_ready = False
        self.last_calculated_data = {}

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

        self.confirm_btn = tk.Button(
            root,
            text="Confirm Trip Destination",
            command=self.handle_confirm_click
        )
        self.confirm_btn.pack(pady=10)
        self.confirm_btn.pack(ipadx=10)
        self.confirm_btn.pack(ipady=15)

    # Displays a welcome greeting to the user.
    def display_username(self):
        greeting = tk.Label(self.root, text=f"Hello! Welcome to PennyPilot", font=("Arial", 14))
        greeting.pack(pady=10) # Add label to window
    
    # Adds a date picker widget for selecting the trip end date.
    def create_date_dropdown(self):
        
        # Create DateEntry widget from tkcalendar
        self.date_entry = DateEntry(self.root, width=21, background='darkblue', foreground='white', borderwidth=2, year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
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

        saved_text = self.int_input.get()
        try:
            already_saved = int(saved_text) if saved_text != "Already Saved" else 0
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer for 'Already Saved'")
            return

        # Run calculation and graph drawing in a separate thread
        threading.Thread(target=self.calculate_in_background, args=(trip, date_str, already_saved)).start()

    # Runs the savings calculation and updates UI tables in a background thread.
    def calculate_in_background(self, trip, date_str, already_saved):
        success, result = calculate_savings_goal(trip[1], date_str, already_saved)
        if success:
            self.result_label.config(text="")

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

    # Fetches and displays a detailed cost breakdown for a trip by category.
    def update_expense_breakdown(self, location):
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

    # Closes the database connection (if active) and gracefully exits the application.
    def on_closing(self):
        """Handle cleanup when window is closed"""
        if self.connector:
            try:
                self.connector.close()
                print("Database connection closed")
            except Exception as e:
                print(f"Error closing database connection: {e}")

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
    
    # Placeholder behavior — clear text on focus if default is shown
    def clear_placeholder(self, event):
     if self.int_input.get() == "Already Saved":
        self.int_input.delete(0, tk.END)
        self.int_input.config(fg='black')

    # Placeholder behavior — restore default text if field is empty
    def add_placeholder(self, event):
        if not self.int_input.get():
            self.int_input.insert(0, "Already Saved")
            self.int_input.config(fg='grey')
    
    def handle_confirm_click(self):
        if not self.calculation_ready:
            messagebox.showerror("Error", "Please calculate trip savings before confirming.")
            return
        show_progress_window(self.last_calculated_data)

    
# Initializes the app after successful login        
def show_main_app(root):
    #app = 
    PennyPilotApp(root)
    #app.mainloop()

# Shows the login popup window
def show_login_window(start_main_app_callback, root):
    import tkinter as tk
    from tkinter import messagebox
    from controllers import handle_login

    # Use a Toplevel window for the login screen
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    
    # Set window size to match main window
    set_window_size(login_window)
    
    # Set up window closing
    setup_window_closing(login_window, root)
    
    # Create a frame to center all content
    main_frame = tk.Frame(login_window)
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Add title
    title_label = tk.Label(main_frame, text="PennyPilot", font=("Arial", 16, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Create a frame for the login form
    login_frame = tk.Frame(main_frame)
    login_frame.pack(expand=True)
    
    # Username
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

    # Password
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

    # Validates login attempt and starts main app if successful
    def attempt_login():
        username = username_entry.get() if username_entry.get() != "Username" else ""
        password = password_entry.get() if password_entry.get() != "Password" else ""
        if handle_login(username, password):
            login_window.destroy()
            root.deiconify()
            start_main_app_callback(root)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    # Button to trigger login check
    login_button = tk.Button(main_frame, text="Login", command=attempt_login)
    login_button.pack(pady=10)
    
    # Create Account button
    create_account_button = tk.Button(main_frame, text="Create Account", 
                                    command=lambda: show_create_account_window(login_window))
    create_account_button.pack(pady=10)

def show_create_account_window(login_window):
    import tkinter as tk
    from tkinter import messagebox
    from database import create_connection
    
    # Hide the login window
    login_window.withdraw()
    
    # Create a new window for account creation
    create_window = tk.Toplevel(login_window)
    create_window.title("Create Account")
    
    # Set window size
    set_window_size(create_window)
    
    # Set up window closing to show login window again
    def on_closing():
        create_window.destroy()
        login_window.deiconify()
    
    create_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Create a frame to center all content
    main_frame = tk.Frame(create_window)
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Add title
    title_label = tk.Label(main_frame, text="Create Account", font=("Arial", 16, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Create a frame for the form
    form_frame = tk.Frame(main_frame)
    form_frame.pack(expand=True)
    
    # Username
    username_label = tk.Label(form_frame, text="Username:", anchor='w')
    username_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
    username_entry = tk.Entry(form_frame)
    username_entry.grid(row=0, column=1, padx=10, pady=5)
    
    # Password
    password_label = tk.Label(form_frame, text="Password:", anchor='w')
    password_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
    password_entry = tk.Entry(form_frame, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=5)
    
    # Confirm Password
    confirm_password_label = tk.Label(form_frame, text="Confirm Password:", anchor='w')
    confirm_password_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
    confirm_password_entry = tk.Entry(form_frame, show='*')
    confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)
    
    # First Name
    first_name_label = tk.Label(form_frame, text="First Name:", anchor='w')
    first_name_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
    first_name_entry = tk.Entry(form_frame)
    first_name_entry.grid(row=3, column=1, padx=10, pady=5)
    
    # Last Name
    last_name_label = tk.Label(form_frame, text="Last Name:", anchor='w')
    last_name_label.grid(row=4, column=0, padx=10, pady=5, sticky='w')
    last_name_entry = tk.Entry(form_frame)
    last_name_entry.grid(row=4, column=1, padx=10, pady=5)
    
    # Email
    email_label = tk.Label(form_frame, text="NAU Email:", anchor='w')
    email_label.grid(row=5, column=0, padx=10, pady=5, sticky='w')
    email_entry = tk.Entry(form_frame)
    email_entry.grid(row=5, column=1, padx=10, pady=5)
    
    def create_account():
        # Get all the values
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        
        # Validate all fields are filled
        if not all([username, password, confirm_password, first_name, last_name, email]):
            messagebox.showerror("Error", "All fields are required")
            return
            
        # Validate passwords match
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
            
            # Check if username already exists
            cursor.execute("SELECT * FROM userProfile WHERE userName = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return
                
            # Insert new user
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
    
    # Create Account button
    create_button = tk.Button(main_frame, text="Create Account", command=create_account)
    create_button.pack(pady=20)

def show_progress_window(data):
    import tkinter as tk
    from tkinter import ttk

    progress_window = tk.Toplevel()
    progress_window.title("Trip Progress")
    set_window_size(progress_window, width=350, height=250)

    progress_window.grab_set()

    # Code to show trip details goes here
    #
    #
    #
    #

    close_button = tk.Button(progress_window, text="Change Destination", command=progress_window.destroy)
    close_button.pack(pady=20)

    setup_window_closing(progress_window)