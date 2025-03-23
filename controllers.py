# Import necessary functions from the database module for backend operations.
from database import (
    add_trip,
    update_savings,
    fetch_financial_data,
    get_trips as db_get_trips,
    get_user_savings,
    get_price_breakdown_by_trip_name
)

# Import date/time utilities to calculate savings timeline.
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Handles logic to validate and add a trip with a destination and cost.
def handle_add_trip(destination, cost):
    try:
        cost = float(cost)
        if cost <= 0:
            return False, "Cost must be greater than 0"
        if not destination.strip():
            return False, "Destination cannot be empty"
        add_trip(destination, cost)
        return True, "Trip added successfully"
    except ValueError:
        return False, "Invalid cost amount"
    except Exception as e:
        return False, str(e)

# Handles logic to update the user's savings, ensuring valid input.
def handle_update_savings(amount):
    try:
        amount = float(amount)
        if amount < 0:
            return False, "Savings amount cannot be negative"
        update_savings(amount)
        return True, "Savings updated"
    except Exception as e:
        return False, str(e)

# Handles fetching all financial data (category, amount) from the database.
def handle_fetch_financial_data():
    try:
        return True, fetch_financial_data()
    except Exception as e:
        return False, str(e)

# Wraps and safely fetches all trips from the database with error handling.
def get_trips():
    try:
        return True, db_get_trips()
    except Exception as e:
        return False, str(e)
    
# Calculates monthly, weekly, and daily savings needed to reach a trip cost by the departure date.
def calculate_savings_goal(trip_cost, departure_date):
    try:
        today = datetime.today().date()
        dep_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
        if dep_date <= today:
            return False, "Departure date must be in the future."

        delta = relativedelta(dep_date, today)
        total_months = delta.years * 12 + delta.months + (1 if delta.days > 0 else 0)

        if total_months == 0:
            return False, "Trip is too close to calculate monthly savings."

        per_month = round(trip_cost / total_months, 2)
        per_week = round(trip_cost / (total_months * 4), 2)
        per_day = round(trip_cost / (total_months * 30), 2)

        return True, {
            "savings_per_month": per_month,
            "savings_per_week": per_week,
            "savings_per_day": per_day
        }
    except Exception as e:
        return False, str(e)
    
# Fetches the cost breakdown for a given trip by name (delegates to DB).
def fetch_trip_expense_breakdown(trip_name):
    return get_price_breakdown_by_trip_name(trip_name)


    
