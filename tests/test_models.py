import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
from models import Finance

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

def test_finance_initialization():
    f = Finance("Savings", 500.0)
    assert f.category == "Savings"
    assert f.amount == 500.0

def test_finance_negative_amount():
    f = Finance("Debt", -100.0)
    assert f.amount == -100.0