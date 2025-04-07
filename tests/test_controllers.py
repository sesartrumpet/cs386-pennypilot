import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import controllers

# Pass functions
def dummy_add_trip(destination, cost):
    # Dummy function that does nothing
    pass

def dummy_update_savings(amount):

    # Dummy function that does nothing
    pass

def dummy_fetch_financial_data():
    return [("Food", 100), ("Transport", 50)]

def dummy_db_get_trips():
    return [("Trip1", 500), ("Trip2", 1000)]

def dummy_get_price_breakdown_by_trip_name(trip_name):

    # Return dummy breakdown for categories:
    # (Travel To, Travel There, Food, Housing, School, Misc)
    return True, (50, 75, 100, 150, 200, 25)

# Test handle_add_trip
def test_handle_add_trip_valid(monkeypatch):
    monkeypatch.setattr(controllers, "add_trip", dummy_add_trip)
    success, message = controllers.handle_add_trip("Paris", "1200")
    assert success is True
    assert message == "Trip added successfully"

def test_handle_add_trip_invalid_cost(monkeypatch):
    monkeypatch.setattr(controllers, "add_trip", dummy_add_trip)
    success, message = controllers.handle_add_trip("Paris", "-100")
    assert success is False
    assert "Cost must be greater than 0" in message

def test_handle_add_trip_invalid_destination(monkeypatch):
    monkeypatch.setattr(controllers, "add_trip", dummy_add_trip)
    success, message = controllers.handle_add_trip("   ", "500")
    assert success is False
    assert "Destination cannot be empty" in message

# Test handle_update_savings
def test_handle_update_savings_valid(monkeypatch):
    monkeypatch.setattr(controllers, "update_savings", dummy_update_savings)
    success, message = controllers.handle_update_savings("300")
    assert success is True
    assert message == "Savings updated"

def test_handle_update_savings_negative(monkeypatch):
    monkeypatch.setattr(controllers, "update_savings", dummy_update_savings)
    success, message = controllers.handle_update_savings("-50")
    assert success is False
    assert "Savings amount cannot be negative" in message

# Test calculate_savings_goal
def test_calculate_savings_goal_valid():
    # Use a future departure date (e.g., 60 days from today)
    future_date = (datetime.today() + timedelta(days=60)).strftime("%Y-%m-%d")
    success, result = controllers.calculate_savings_goal(1200, future_date)
    assert success is True

    # Calculate expected total months using relativedelta
    today = datetime.today().date()
    dep_date = datetime.strptime(future_date, "%Y-%m-%d").date()
    delta = relativedelta(dep_date, today)
    total_months = delta.years * 12 + delta.months + (1 if delta.days > 0 else 0)
    expected_per_month = round(1200 / total_months, 2)
    assert result["savings_per_month"] == expected_per_month

def test_calculate_savings_goal_past_date():
    past_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    success, message = controllers.calculate_savings_goal(1200, past_date)
    assert success is False
    assert "Departure date must be in the future" in message

# Test get_trips
def test_get_trips(monkeypatch):
    monkeypatch.setattr(controllers, "db_get_trips", dummy_db_get_trips)
    success, trips = controllers.get_trips()
    assert success is True
    assert isinstance(trips, list)
    assert len(trips) > 0

# Test handle_fetch_financial_data
def test_handle_fetch_financial_data(monkeypatch):
    monkeypatch.setattr(controllers, "fetch_financial_data", dummy_fetch_financial_data)
    success, data = controllers.handle_fetch_financial_data()
    assert success is True
    assert isinstance(data, list)
    assert data[0][0] == "Food"

# Test fetch_trip_expense_breakdown
def test_fetch_trip_expense_breakdown(monkeypatch):
    monkeypatch.setattr(controllers, "get_price_breakdown_by_trip_name", dummy_get_price_breakdown_by_trip_name)
    success, breakdown = controllers.fetch_trip_expense_breakdown("Trip1")

    # Expect breakdown to be a tuple (or list) with 6 values
    assert isinstance(breakdown, (tuple, list))
    assert len(breakdown) == 6
