import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from datetime import date, timedelta
import gui
from gui import set_window_size

# Test the generate_future_dates function
def test_generate_future_dates():
    dates = gui.generate_future_dates()
    assert isinstance(dates, list)
    assert len(dates) == 30
    today = date.today()
    # The first date should be tomorrow
    assert dates[0] == today + timedelta(days=1)

# Fixture to create a PennyPilotApp instance
@pytest.fixture
def app_instance(monkeypatch):
    # Monkeypatch get_trips (imported from controllers) to return dummy data
    dummy_trips = [("TestUser", 1000)]
    monkeypatch.setattr(gui, "get_trips", lambda: (True, dummy_trips))
    root = tk.Tk()
    # Hide the window during tests
    root.withdraw()
    app = gui.PennyPilotApp(root, username="dummy")
    yield app
    # Destroy the window after test
    root.destroy()

def test_app_initialization(app_instance):
    app = app_instance
    # Check that key UI components are initialized
    assert hasattr(app, "trip_dropdown")
    assert hasattr(app, "date_entry")
    assert hasattr(app, "savings_table")
    assert hasattr(app, "expense_breakdown_table")

def test_calculate_in_background(app_instance, monkeypatch):
    # Create a dummy savings result
    dummy_result = {
        "savings_per_month": 100,
        "savings_per_week": 25,
        "savings_per_day": 3.33
    }
    # Monkey-patch calculate_savings_goal to return dummy_result
    monkeypatch.setattr(gui, "calculate_savings_goal", lambda trip_cost, departure_date, already_saved: (True, dummy_result))
    # Monkey-patch update_expense_breakdown to do nothing
    monkeypatch.setattr(app_instance, "update_expense_breakdown", lambda location: None)
    
    # Call calculate_in_background with a dummy trip and a future date
    app_instance.calculate_in_background(("TestUser", 1000), "2099-12-31", 0)
    
    # Retrieve updated table items
    month_item = app_instance.savings_table.item("month")["values"]
    week_item = app_instance.savings_table.item("week")["values"]
    day_item = app_instance.savings_table.item("day")["values"]
    
    # Check that the values contain the dummy results (as strings with a dollar sign)
    assert "100" in month_item[1]
    assert "25" in week_item[1]
    assert "3.33" in day_item[1]

def test_update_expense_breakdown(app_instance, monkeypatch):
    # Create dummy breakdown data for 6 categories
    dummy_breakdown = (50, 75, 100, 150, 200, 25)
    # Monkey-patch fetch_trip_expense_breakdown to return success and dummy_breakdown
    monkeypatch.setattr(gui, "fetch_trip_expense_breakdown", lambda trip_name: (True, dummy_breakdown))
    # Call update_expense_breakdown with a dummy location
    app_instance.update_expense_breakdown("TestUser")
    
    # Check one of the updated items; for instance, "travelto" should now show the dummy value
    travelto_item = app_instance.expense_breakdown_table.item("travelto")["values"]
    total_item = app_instance.expense_breakdown_table.item("total")["values"]
    
    # Validate that the travel cost is formatted (e.g., "$50.00")
    assert "$50" in travelto_item[1]
    # Validate that total equals the sum of dummy_breakdown values
    expected_total = sum(dummy_breakdown)
    assert f"${expected_total:,.2f}" in total_item[1]

@pytest.mark.skip(reason="Tkinter cannot initialize in headless test environment")
def test_set_window_size_runs():
    root = tk.Tk()
    try:
        set_window_size(root, 500, 500)
    finally:
        root.destroy()