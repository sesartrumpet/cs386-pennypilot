# import MySQL connector driver manager
import mysql.connector
import os
import warnings


def run_sql_file(cursor, filepath):
    if not os.path.exists(filepath):
        print(f"SQL file not found: {filepath}")
        return

    with open(filepath, 'r') as file:
        sql = file.read()
        for statement in sql.split(';'):
            if statement.strip():
                try:
                    cursor.execute(statement)
                except mysql.connector.Error as err:
                    print(f"Error executing statement: {err}")


# main program
def main(config):
    # open the database connection
    connector = mysql.connector.Connect(**config)
    # check if the connection is open
    print("Is connected?", connector.is_connected())

    # print the server's version
    print("MySQL Server version:", connector.get_server_info())
    cursor = connector.cursor()
    warnings.filterwarnings("ignore", category=UserWarning)
    print("Initializing database...")
    run_sql_file(cursor, 'PennyPilot_db.sql')
    run_sql_file(cursor, 'Penny_data.sql')
    connector.commit()
    print("Database initialized.")

    # fetch and print userProfile data
    cursor.execute("SELECT * FROM userProfile")
    rows = cursor.fetchall()
    print("userProfile data:")
    for row in rows:
        print(row)

    cursor.close()
    connector.close()

# checks whether the script is being run as the main program
if __name__ == '__main__':
    #  import the config module
    import config as myconfig

    #
    # Configure MySQL login and database to use in config.py
    # This line returns a dictionary containing MySQL credentials and
    # database information
    # copy() is used to ensure a shallow copy of the dictionary and avoid
    # unintentional modifications to the original connection details
    config = myconfig.Config.dbinfo().copy()
    print("Connecting with config:", config)
    # calls the main function passing the config dictionary
    main(config)


def add_trip(destination, cost):
    connector = create_connection()
    cursor = connector.cursor()
    cursor.execute("INSERT INTO trip (destination, cost) VALUES (%s, %s)", (destination, cost))
    connector.commit()
    cursor.close()
    connector.close()

def update_savings(amount):
    connector = create_connection()
    cursor = connector.cursor()
    cursor.execute("SELECT id FROM finances WHERE category = 'Savings'")
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE finances SET amount = %s WHERE category = 'Savings'", (amount,))
    else:
        cursor.execute("INSERT INTO finances (category, amount) VALUES ('Savings', %s)", (amount,))
    connector.commit()
    cursor.close()
    connector.close()

def fetch_financial_data():
    connector = create_connection()
    cursor = connector.cursor()
    cursor.execute("SELECT category, amount FROM finances")
    records = cursor.fetchall()
    cursor.close()
    connector.close()
    return records

def get_user_savings():
    connector = create_connection()
    cursor = connector.cursor()
    cursor.execute("SELECT amount FROM finances WHERE category = 'Savings'")
    row = cursor.fetchone()
    cursor.close()
    connector.close()
    return float(row[0]) if row else 0.0

def get_trips():
    connector = create_connection()
    cursor = connector.cursor()
    cursor.execute("""
        SELECT d.location, 
        (p.Travelto + p.Travelthere + p.Food + p.Housing + p.School + p.Misc) as total_cost
        FROM tripDestination d
        JOIN prices p ON d.location = p.location
    """)
    trips = cursor.fetchall()
    cursor.close()
    connector.close()
    return trips


def get_price_breakdown_by_location(location):
    connector = create_connection()
    cursor = connector.cursor()
    cursor.execute("""
        SELECT Travelto, Travelthere, Food, Housing, School, Misc 
        FROM prices WHERE location = %s
    """, (location,))
    row = cursor.fetchone()
    cursor.close()
    connector.close()
    
    if not row:
        return []
    
    categories = ["Travel To", "Travel There", "Food", "Housing", "School", "Misc"]
    return list(zip(categories, row))

def create_connection():
    import config as myconfig
    config = myconfig.Config.dbinfo().copy()
    try:
        print(f"Attempting to connect to MySQL with config: {config}")
        connector = mysql.connector.Connect(**config)
        print("Successfully connected to MySQL")
        return connector
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        print(f"Error code: {err.errno}")
        print(f"SQL State: {err.sqlstate}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

