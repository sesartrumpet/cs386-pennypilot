from database import (
    add_trip,
    update_savings,
    fetch_financial_data,
    create_tables
)

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
