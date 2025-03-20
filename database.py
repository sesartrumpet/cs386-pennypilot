import mysql.connector

# Settings to connect database
DB_CONFIG = {"host": "localhost",
            "user": "your_username",
            "password": "your_password",
            "database": "penny_pilot"}

# function to connect to database
def create_connection():
    """Establish a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)

# function to connect to database using 
def create_tables():
    """Creates necessary tables for the application."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finances (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(255),
            amount DECIMAL(10,2)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INT AUTO_INCREMENT PRIMARY KEY,
            destination VARCHAR(255),
            cost DECIMAL(10,2)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def add_trip(destination, cost):
    """Inserts a new trip into the database."""
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO trips (destination, cost) VALUES (%s, %s)"
    cursor.execute(query, (destination, cost))

    conn.commit()
    cursor.close()
    conn.close()

def update_savings(amount):
    """Updates the savings amount in the database."""
    conn = create_connection()
    cursor = conn.cursor()

    query = "UPDATE finances SET amount = %s WHERE category = 'Savings'"
    cursor.execute(query, (amount,))

    conn.commit()
    cursor.close()
    conn.close()

def fetch_financial_data():
    """Fetches all financial records from the database."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT category, amount FROM finances")
    records = cursor.fetchall()

    cursor.close()
    conn.close()
    return records
