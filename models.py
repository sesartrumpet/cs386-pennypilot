# Define the finance class to represent a financial record
class Finance:
  # The constructor initializes the finance object with a category and an amount 
    def __init__(self, category, amount):
        self.category = category
        self.amount = amount

# Define the Trip class to prevent a trip with a destination and associated cost
class Trip:
  
  #   # The constructor initializes the Trip object with a destination and a cost
  def __init__(self, destination, cost):
        self.destination = destination
        self.cost = cost