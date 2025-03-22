import tkinter as tk
from tkinter import ttk, messagebox
from controllers import get_trips, calculate_savings_goal, handle_update_savings
from database import get_user_savings
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PennyPilotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Penny Pilot - Trip Savings")

        # Dropdown for trip
        self.trip_var = tk.StringVar()
        success, result = get_trips()
        if success:
            self.trips = result
        else:
            self.trips = []
            messagebox.showerror("Database Error", result)

        
        #self.trips = get_trips()[1]
        
        
        self.trip_dropdown = ttk.Combobox(root, textvariable=self.trip_var, state="readonly")
        
        
        self.trip_dropdown["values"] = [f"{trip[0]} - {trip[1]} (${trip[2]})" for trip in self.trips]
        
        #self.trip_dropdown["values"] = [f"{trip[0]} - {trip[1]} (${trip[2]})" for trip in self.trips]

        
        
        self.trip_dropdown.pack(pady=5)

        # Date input
        self.date_label = tk.Label(root, text="Enter trip date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(root)
        self.date_entry.pack(pady=5)

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


        

        # Graph frame
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack()

    def calculate(self):
        selected = self.trip_var.get()
        if not selected:
            return
        trip_id = int(selected.split(" - ")[0])
        trip = next(t for t in self.trips if t[0] == trip_id)
        date_str = self.date_entry.get()
        success, result = calculate_savings_goal(trip[2], date_str)
        if success:
            self.result_label.config(text="")

            # Clear table
            for row in self.savings_table.get_children():
                self.savings_table.delete(row)

            if success:
                self.result_label.config(text="")

                self.savings_table.item("month", values=("Monthly", f"${result['savings_per_month']}"))
                self.savings_table.item("week", values=("Weekly", f"${result['savings_per_week']}"))
                self.savings_table.item("day", values=("Daily", f"${result['savings_per_day']}"))

                self.draw_graph(get_user_savings(), trip[2])
            else:
                self.savings_table.item("month", values=("Monthly", "—"))
                self.savings_table.item("week", values=("Weekly", "—"))
                self.savings_table.item("day", values=("Daily", "—"))
                messagebox.showerror("Error", result)


            self.draw_graph(get_user_savings(), trip[2])
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
                    trip_id = int(selected.split(" - ")[0])
                    trip = next(t for t in self.trips if t[0] == trip_id)
                    self.draw_graph(amount, trip[2])
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")

    def draw_graph(self, saved, goal):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig = plt.Figure(figsize=(4,2))
        ax = fig.add_subplot(111)
        ax.bar(['Goal'], [goal], color='lightgray')
        ax.bar(['Current'], [saved], color='green')
        ax.set_ylim(0, max(goal, saved + 50))
        ax.set_ylabel("Amount Saved")
        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()
