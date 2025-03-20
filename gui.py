import tkinter as tk
from tkinter import ttk
from controllers import handle_add_trip, handle_update_savings

class PennyPilotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Penny Pilot")

        # Layout: Left Panel (Student Info)
        self.left_panel = tk.Frame(root, width=200, height=500)
        self.left_panel.pack(side="left", fill="y")

        tk.Label(self.left_panel, text="Student Info").pack()
        self.income_btn = tk.Button(self.left_panel, text="Income", command=self.show_income)
        self.income_btn.pack()

        self.expenses_btn = tk.Button(self.left_panel, text="Expenses", command=self.show_expenses)
        self.expenses_btn.pack()

        self.savings_btn = tk.Button(self.left_panel, text="Savings", command=self.show_savings)
        self.savings_btn.pack()

        # Monies Breakdown (Table)
        self.table_frame = tk.Frame(root, width=400, height=300)
        self.table_frame.pack(side="top", fill="both", expand=True)

        self.tree = ttk.Treeview(self.table_frame, columns=("Category", "Amount"), show="headings")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.pack(fill="both", expand=True)

        # Right Panel (Trips)
        self.right_panel = tk.Frame(root, width=200, height=500)
        self.right_panel.pack(side="right", fill="y")

        self.trip_button = tk.Button(self.right_panel, text="Add Trip", command=handle_add_trip)
        self.trip_button.pack()

        self.goal_label = tk.Label(root, text="Goal:")
        self.goal_label.pack()

        self.goal_entry = tk.Entry(root)
        self.goal_entry.pack()

        self.save_goal_btn = tk.Button(root, text="Save", command=handle_update_savings)
        self.save_goal_btn.pack()

    def show_income(self):
        print("Displaying income")

    def show_expenses(self):
        print("Displaying expenses")

    def show_savings(self):
        print("Displaying savings")
