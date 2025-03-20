# Import tkinter for creating the GUI
import tkinter as tk
# Importing ttk for creating more advanced widgets( like Treeview)
from tkinter import ttk
# Importing functions for handling trip addition and savings update
from controllers import handle_add_trip, handle_update_savings
# Defining the main class for the PennyPilot application
class PennyPilotApp:
    # Initializer function to set up the main window and its elements
    def __init__(self, root):
        # Assign the root window to the class instance
        self.root = root
        # Set the title of the main window
        self.root.title("Penny Pilot")

        # Layout: Left Panel (Student Info)
        # Create a left panel to display student info
        self.left_panel = tk.Frame(root, width=200, height=500)
        # Pack the left panel to the left side, filling vertically
        self.left_panel.pack(side="left", fill="y")

        # Add a label for "Student Info" in the left panel
        tk.Label(self.left_panel, text="Student Info").pack()
        # Create a button for showing income
        self.income_btn = tk.Button(self.left_panel, text="Income", command=self.show_income)
        # Pack the income button
        self.income_btn.pack()

        # Create a button for showing expenses
        self.expenses_btn = tk.Button(self.left_panel, text="Expenses", command=self.show_expenses)
        # Pack the savings button
        self.expenses_btn.pack()

        self.savings_btn = tk.Button(self.left_panel, text="Savings", command=self.show_savings)
        self.savings_btn.pack()

        # Monies Breakdown (Table)
        # Create a frame for the table that shows the money breakdown
        self.table_frame = tk.Frame(root, width=400, height=300)
        # Pack the table frame to the top, allowing it to expand
        self.table_frame.pack(side="top", fill="both", expand=True)

        
        # Create a Treeview to display categories and amounts
        self.tree = ttk.Treeview(self.table_frame, columns=("Category", "Amount"), show="headings")
        # Set the heading for the "Category" column
        self.tree.heading("Category", text="Category")
        # Set the heading for the "Amount" column
        self.tree.heading("Amount", text="Amount")
        # Pack the Treeview into the frame, allowing it to expand
        self.tree.pack(fill="both", expand=True)

        # Right Panel (Trips)
        # Create a right panel for managing trips
        self.right_panel = tk.Frame(root, width=200, height=500)
         # Pack the right panel to the right side, filling vertically
        self.right_panel.pack(side="right", fill="y")

        # Create a button to add a trip, calling the handle_add_trip function
        self.trip_button = tk.Button(self.right_panel, text="Add Trip", command=handle_add_trip)
        # Pack the add trip button
        self.trip_button.pack()

        # Create a label for the goal entry
        self.goal_label = tk.Label(root, text="Goal:")
        # Pack the goal label
        self.goal_label.pack()

        # Create an entry field for the user to input their goal
        self.goal_entry = tk.Entry(root)
        # Pack the goal entry field
        self.goal_entry.pack()

        # Create a button to save the goal, calling the handle_update_savings function
        self.save_goal_btn = tk.Button(root, text="Save", command=handle_update_savings)
        # Pack the save goal button
        self.save_goal_btn.pack()

    # Define the method to display income (prints a message for now)
    def show_income(self):
        print("Displaying income")

    # Define the method to display expenses (prints a message for now)
    def show_expenses(self):
        print("Displaying expenses")

    # Define the method to display savings (prints a message for now)
    def show_savings(self):
        print("Displaying savings")
