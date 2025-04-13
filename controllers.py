"""
This module contains the business logic and controllers for the PennyPilot application.
It handles all the core functionality including trip management, savings calculations,
and user authentication.
"""

from database import (
    add_trip,
    update_savings,
    get_trips as db_get_trips,
    get_user_savings,
    get_price_breakdown_by_trip_name,
    authenticate_user
)

from datetime import datetime
from dateutil.relativedelta import relativedelta

def handle_add_trip(destination, cost):
    """
    Handles the addition of a new trip to the database.
    
    Args:
        destination (str): The name of the trip destination
        cost (float): The total cost of the trip
        
    Returns:
        tuple: (success: bool, message: str)
            - success: True if trip was added successfully, False otherwise
            - message: Success message or error description
    """
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

def handle_update_savings(amount, username=None):
    """
    Updates the user's savings amount in the database.
    
    Args:
        amount (float): The new savings amount
        username (str, optional): The username to update savings for
        
    Returns:
        tuple: (success: bool, message: str)
            - success: True if savings were updated successfully, False otherwise
            - message: Success message or error description
    """
    try:
        amount = float(amount)
        if amount < 0:
            return False, "Savings amount cannot be negative"
            
        if update_savings(amount, username):
            return True, "Savings updated successfully"
        else:
            return False, "No active trip found to update"
            
    except ValueError:
        return False, "Invalid amount format"
    except Exception as e:
        return False, str(e)

def get_trips():
    """
    Retrieves all available trips and their total costs.
    
    Returns:
        tuple: (success: bool, trips: list)
            - success: True if trips were fetched successfully, False otherwise
            - trips: List of (destination, total_cost) tuples or error message
    """
    try:
        return True, db_get_trips()
    except Exception as e:
        return False, str(e)

def calculate_savings_goal(trip_cost, departure_date, already_saved=0):
    """
    Calculates the required savings goals (daily, weekly, monthly) for a trip.
    
    Args:
        trip_cost (float): Total cost of the trip
        departure_date (str): Date of departure in YYYY-MM-DD format
        already_saved (float): Amount already saved for the trip
        
    Returns:
        tuple: (success: bool, result: dict)
            - success: True if calculation was successful, False otherwise
            - result: Dictionary containing savings goals or error message
                {
                    'savings_per_month': float,
                    'savings_per_week': float,
                    'savings_per_day': float
                }
    """
    try:
        today = datetime.today().date()
        dep_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
        trip_cost = max(0, trip_cost - already_saved)

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
    
def fetch_trip_expense_breakdown(location):
    """
    Fetches the detailed expense breakdown for a specific trip location.
    
    Args:
        location (str): The name of the trip location
        
    Returns:
        tuple: (success: bool, data: list)
            - success: True if data was fetched successfully, False otherwise
            - data: List of expense categories and their costs or error message
    """
    try:
        success, data = get_price_breakdown_by_trip_name(location)
        return success, data
    except Exception as e:
        return False, str(e)

def handle_login(username, password):
    """
    Handles user authentication.
    
    Args:
        username (str): User's username
        password (str): User's password
        
    Returns:
        bool: True if authentication was successful, False otherwise
    """
    return authenticate_user(username, password)


