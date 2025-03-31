import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models

def test_finance_creation():
    finance = models.Finance("Food", 150.75)
    assert hasattr(finance, "category")
    assert hasattr(finance, "amount")
    assert finance.category == "Food"
    assert finance.amount == 150.75

def test_trip_creation():
    trip = models.Trip("Paris", 1200)
    assert hasattr(trip, "destination")
    assert hasattr(trip, "cost")
    assert trip.destination == "Paris"
    assert trip.cost == 1200