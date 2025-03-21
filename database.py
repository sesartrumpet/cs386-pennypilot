import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",  # Use your actual password
    "database": "pennypilot_db"  # Change this from "penny_pilot" to "pennypilot_db"
}



def create_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_tables():
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
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO trips (destination, cost) VALUES (%s, %s)", (destination, cost))
    conn.commit()
    cursor.close()
    conn.close()

def update_savings(amount):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM finances WHERE category = 'Savings'")
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE finances SET amount = %s WHERE category = 'Savings'", (amount,))
    else:
        cursor.execute("INSERT INTO finances (category, amount) VALUES ('Savings', %s)", (amount,))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_financial_data():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, amount FROM finances")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

def get_user_savings():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM finances WHERE category = 'Savings'")
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return float(row[0]) if row else 0.0

def get_trips():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, destination, cost FROM trips")
    trips = cursor.fetchall()
    cursor.close()
    conn.close()
    return trips
