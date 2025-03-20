# Define the finance class to represent a financial record
class Finance:
  # The constructor initializes the finance object with a category and an amount 
    def __init__(self, category, amount):
      # Set the category attribute to the given category value
        self.category = category
      # Set the amount attribute to the given amount value
        self.amount = amount

# Define the Trip class to prevent a trip with a destination and associated cost
class Trip:
  
  #   # The constructor initializes the Trip object with a destination and a cost
  def __init__(self, destination, cost):
      # Set the destination attribute to the given destination value
        self.destination = destination
      # Set the cost attribute to the given cost value
        self.cost = cost
