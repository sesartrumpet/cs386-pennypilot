import tkinter as tk
from tkinter import ttk, messagebox
from controllers import get_trips, calculate_savings_goal, handle_update_savings, fetch_trip_expense_breakdown
from database import get_user_savings
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar
import datetime
import threading
import mysql.connector

def generate_future_dates():
    today = datetime.date.today()
    future_dates = []
    for i in range(1, 31):  # Example: Generate 30 days of future dates
        future_dates.append(today + datetime.timedelta(days=i))
    return future_dates


class PennyPilotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Penny Pilot - Trip Savings")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.connector = None  # Initialize database connection variable

        # Dropdown for trip
        self.trip_var = tk.StringVar()
        success, result = get_trips()
        if success:
            self.trips = result
        else:
            self.trips = []
            messagebox.showerror("Database Error", result)

        self.trip_dropdown = ttk.Combobox(root, textvariable=self.trip_var, state="readonly")
        self.trip_dropdown["values"] = [f"{trip[0]} - {trip[1]} (${trip[2]:.2f})" for trip in self.trips]
        self.trip_dropdown.pack(pady=5)

        # Date input with calendar widget
        self.create_date_dropdown()

        # Calculate button
        self.calc_btn = tk.Button(root, text="Calculate Savings Goal", command=self.calculate)
        self.calc_btn.pack(pady=5)

        # Savings input
        self.savings_label = tk.Label(root, text="Update current savings:")
        self.savings_label.pack()
        self.savings_entry = tk.Entry(root)
        self.savings_entry.pack()
        self.savings_btn = tk.Button(root, text="Update Savings", command=self.update_savings)
        self.savings_btn.pack()

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

        # Graph frame
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack()

        # Show initial empty graph
        self.draw_graph(0, 0)

    def create_date_dropdown(self):
        # Create DateEntry widget from tkcalendar
        self.date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2, year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        self.date_entry.pack(pady=5)

    def calculate(self):
        selected = self.trip_var.get()
        if not selected:
            return
        username = selected.split(" - ")[0]  # Now getting username instead of trip_id
        trip = next(t for t in self.trips if t[0] == username)

        # Get the selected date from the calendar widget
        date_str = self.date_entry.get_date().strftime("%Y-%m-%d")

        # Run calculation and graph drawing in a separate thread
        threading.Thread(target=self.calculate_in_background, args=(trip, date_str)).start()

    def calculate_in_background(self, trip, date_str):
        success, result = calculate_savings_goal(trip[2], date_str)
        if success:
            self.result_label.config(text="")

            self.savings_table.item("month", values=("Monthly", f"${result['savings_per_month']}"))
            self.savings_table.item("week", values=("Weekly", f"${result['savings_per_week']}"))
            self.savings_table.item("day", values=("Daily", f"${result['savings_per_day']}"))

            self.draw_graph(get_user_savings(), trip[2])

            # Show breakdown of expenses for the selected location
            success, expenses = fetch_trip_expense_breakdown(trip[1])  # trip[1] = location
            if success:
                # Category to Treeview row ID mapping
                category_ids = {
                    "Travel To": "travelto",
                    "Travel There": "travelthere",
                    "Food": "food",
                    "Housing": "housing",
                    "School": "school",
                    "Misc": "misc"
                }

                # Map DB results to a dictionary
                amounts = {category: cost for category, cost in expenses}
                total = 0

                for label, iid in category_ids.items():
                    amount = amounts.get(label, 0.0)
                    total += amount
                    self.expense_breakdown_table.item(iid, values=(label, f"${amount:.2f}"))

                self.expense_breakdown_table.item("total", values=("Total", f"${total:.2f}"))
            else:
                messagebox.showerror("Error", f"Could not load breakdown: {expenses}")
        else:
            messagebox.showerror("Error", result)

    def update_savings(self):
        try:
            amount = float(self.savings_entry.get())
            success, msg = handle_update_savings(amount)
            if success:
                messagebox.showinfo("Success", msg)
                selected = self.trip_var.get()
                if selected:
                    username = selected.split(" - ")[0]
                    trip = next(t for t in self.trips if t[0] == username)
                    self.draw_graph(amount, trip[2])
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")

    def draw_graph(self, saved=0, goal=0):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig = plt.Figure(figsize=(5.5, 1.6))
        ax = fig.add_subplot(111)

        # Avoid division by zero
        goal = goal if goal > 0 else 1
        target_progress = min(saved / goal, 1)

        # Style
        label_size = 8
        y_offset = 0.15
        bar_height = 0.5

        you_are_here = "You are\nhere"
        penny_pilot_msg = "PennyPilot\nhelps you\nget here"

        bar_container = ax.barh([''], [0], color='green', height=bar_height)

        # Draw faded remaining portion (light gray with alpha)
        ax.barh([''], [1], left=0, color='lightgray', height=bar_height, alpha=0.3)

        # Set fixed display
        ax.set_xlim(0, 1)
        ax.axis("off")

        # Text annotations
        value_label = ax.text(0.5, -0.4, "", ha="center", fontsize=9, fontweight="bold")
        you_here_label = ax.text(0, y_offset, you_are_here, fontsize=label_size, fontweight="bold",
                                color="white", backgroundcolor="green", ha="left")
        penny_msg_label = ax.text(0.99, y_offset, penny_pilot_msg, fontsize=label_size,
                                fontweight="bold", color="black", ha="right")

        def update(frame):
            progress = min(frame / 100, target_progress)
            bar_container[0].set_width(progress)

            # Update dollar value display
            current_val = progress * goal
            value_label.set_text(f"${current_val:,.2f} of ${goal:,.2f}")

            # Move "You are here"
            x_pos = max(progress * 0.98, 0.01)
            align = "right" if progress > 0.1 else "left"
            you_here_label.set_position((x_pos, y_offset))
            you_here_label.set_ha(align)

            return bar_container

        anim = animation.FuncAnimation(fig, update, frames=101, interval=10, repeat=False)

        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def on_closing(self):
        """Handle cleanup when window is closed"""
        if self.connector:
            try:
                self.connector.close()
                print("Database connection closed")
            except Exception as e:
                print(f"Error closing database connection: {e}")
        self.root.destroy()

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
