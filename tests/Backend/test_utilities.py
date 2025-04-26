import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utilities import format_currency

def test_format_currency():
    assert format_currency(12) == "$12.00"
    assert format_currency(12.5) == "$12.50"
    assert format_currency(0) == "$0.00"

def test_format_currency_basic():
    assert format_currency(1234.5) == "$1,234.50"

def test_format_currency_negative():
    assert format_currency(-99.99) == "$-99.99"

def test_format_currency_zero():
    assert format_currency(0) == "$0.00"