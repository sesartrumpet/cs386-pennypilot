from database import (
    add_trip,
    update_savings,
    fetch_financial_data,
    create_tables,
    create_connection
)
from datetime import datetime

def initialize_database():
    """Initialize the database and create necessary tables."""
    create_tables()

def handle_add_trip(destination, cost):
    """Handle the addition of a new trip."""
    try:
        cost = float(cost)  # Convert cost to float
        if cost <= 0:
            return False, "Cost must be greater than 0"
        if not destination.strip():
            return False, "Destination cannot be empty"
            
        add_trip(destination, cost)
        return True, "Trip added successfully"
    except ValueError:
        return False, "Invalid cost amount"
    except Exception as e:
        return False, f"Error adding trip: {str(e)}"

def handle_update_savings(amount):
    """Handle updating the savings amount."""
    try:
        amount = float(amount)  # Convert amount to float
        if amount < 0:
            return False, "Savings amount cannot be negative"
            
        update_savings(amount)
        return True, "Savings updated successfully"
    except ValueError:
        return False, "Invalid savings amount"
    except Exception as e:
        return False, f"Error updating savings: {str(e)}"

def handle_fetch_financial_data():
    """Handle fetching all financial data."""
    try:
        records = fetch_financial_data()
        return True, records
    except Exception as e:
        return False, f"Error fetching financial data: {str(e)}"

def get_trips():
    """Fetches all trips from the database."""
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, destination, cost, timeframe FROM trips")
        trips = cursor.fetchall()

        cursor.close()
        conn.close()
        return True, trips
    except Exception as e:
        return False, f"Error fetching trips: {str(e)}"

def calculate_savings_goal(trip_cost, timeframe):
    """Calculates savings needed per month, week, and day to reach the trip goal.
    Args:
        trip_cost: Total cost of the trip
        timeframe: Number of months until the trip
    """
    try:
        if timeframe <= 0:
            return False, "Timeframe must be greater than 0 months"

        # Convert months to days (approximate)
        days_remaining = timeframe * 30

        savings_per_month = round(trip_cost / timeframe, 2)
        savings_per_week = round(trip_cost / (timeframe * 4), 2)  # Assuming 4 weeks per month
        savings_per_day = round(trip_cost / days_remaining, 2)

        return True, {
            "savings_per_month": savings_per_month,
            "savings_per_week": savings_per_week,
            "savings_per_day": savings_per_day,
        }
    except ValueError:
        return False, "Invalid timeframe or cost value"
    except Exception as e:
        return False, f"Error calculating savings goal: {str(e)}"
