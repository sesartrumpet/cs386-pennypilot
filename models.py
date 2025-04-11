"""
This module contains the data models used throughout the PennyPilot application.
These classes represent the core data structures and provide a clean interface
for working with financial and trip data.
"""

# Define the finance class to represent a financial record
class Finance:
    """
    Represents a financial record in the system.
    
    Attributes:
        category (str): The category of the financial record (e.g., 'Savings', 'Expense')
        amount (float): The monetary amount associated with the record
    """
    # The constructor initializes the finance object with a category and an amount 
    def __init__(self, category, amount):
        """
        Initialize a new financial record.
        
        Args:
            category (str): The category of the financial record
            amount (float): The monetary amount
        """
        self.category = category
        self.amount = amount

# Define the Trip class to prevent a trip with a destination and associated cost
class Trip:
    """
    Represents a travel destination and its associated costs.
    
    Attributes:
        destination (str): The name of the travel destination
        cost (float): The total estimated cost of the trip
    """
    #   # The constructor initializes the Trip object with a destination and a cost
    def __init__(self, destination, cost):
        """
        Initialize a new trip record.
        
        Args:
            destination (str): The name of the travel destination
            cost (float): The total estimated cost
        """
        self.destination = destination
        self.cost = cost