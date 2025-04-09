# import MySQL connector driver manager
import mysql.connector
import os
import warnings
from pathlib import Path

def create_database_if_not_exists(config):
    """Creates the database if it doesn't exist."""
    try:
        # Remove database from config temporarily
        db_name = config.pop('database', 'pennypilot_db')
        
        # Connect to MySQL without specifying a database
        connector = mysql.connector.Connect(**config)
        cursor = connector.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        connector.commit()
        
        # Restore database name to config
        config['database'] = db_name
        
        cursor.close()
        connector.close()
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

# Executes SQL statements from a provided file using the given cursor.
def run_sql_file(cursor, filepath):
    if not os.path.exists(filepath):
        print(f"SQL file not found: {filepath}")
        return False

    with open(filepath, 'r') as file:
        sql = file.read()
        for statement in sql.split(';'):
            if statement.strip():
                try:
                    cursor.execute(statement)
                except mysql.connector.Error as err:
                    print(f"Error executing statement: {err}")
                    return False
    return True

def initialize_database(config=None, verbose=True):
    """
    Initializes the database by running the setup scripts.
    Args:
        config (dict, optional): Database configuration. If None, will use config from config.py
        verbose (bool): Whether to print detailed information about the initialization process
    Returns:
        bool: True if initialization was successful, False otherwise
    """
    try:
        if config is None:
            import config as myconfig
            config = myconfig.Config.dbinfo().copy()
        
        # First ensure the database exists
        if not create_database_if_not_exists(config):
            print("Failed to create database")
            return False
            
        # Now connect to the specific database
        connector = mysql.connector.Connect(**config)
        cursor = connector.cursor()
        warnings.filterwarnings("ignore", category=UserWarning)
        
        if verbose:
            print("Is connected?", connector.is_connected())
            print("MySQL Server version:", connector.get_server_info())
            print("Initializing database...")
        
        # Get the directory where this script is located
        script_dir = Path(__file__).parent.absolute()
        
        # Run the SQL files
        db_success = run_sql_file(cursor, script_dir / 'PennyPilot_db.sql')
        data_success = run_sql_file(cursor, script_dir / 'data.sql')
        
        if not (db_success and data_success):
            print("Failed to execute one or more SQL files")
            return False
            
        connector.commit()
        
        if verbose:
            print("Database initialized successfully.")
            # Print some initial data to verify setup
            cursor.execute("SELECT * FROM userProfile")
            rows = cursor.fetchall()
            print("userProfile data:")
            for row in rows:
                print(row)
        
        cursor.close()
        connector.close()
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

# checks whether the script is being run as the main program
if __name__ == '__main__':
    import config as myconfig
    config = myconfig.Config.dbinfo().copy()
    print("Connecting with config:", config)
    initialize_database(config)

# Inserts a new trip into the 'trip' table with a given destination and cost.
def add_trip(destination, cost):
    connector = create_connection()
    cursor = connector.cursor()
    cursor.execute("INSERT INTO trip (destination, cost) VALUES (%s, %s)", (destination, cost))
    connector.commit()
    cursor.close()
    connector.close()

# Updates or inserts a savings amount into the 'finances' table under the 'Savings' category.
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

# Fetches all records from the 'finances' table as a list of (category, amount) tuples
def fetch_financial_data():
    connector = create_connection()
    cursor = connector.cursor()
    cursor.execute("SELECT category, amount FROM finances")
    records = cursor.fetchall()
    cursor.close()
    connector.close()
    return records

# Retrieves the current user's savings amount from the 'finances' table.
def get_user_savings():
    connector = create_connection()
    cursor = connector.cursor()
    cursor.execute("SELECT amount FROM finances WHERE category = 'Savings'")
    row = cursor.fetchone()
    cursor.close()
    connector.close()
    return float(row[0]) if row else 0.0

# Retrieves a list of all trips and their total costs by summing up the category columns from the 'prices' table.
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

# Retrieves the breakdown of cost categories (Travelto, Travelthere, Food, Housing, School, Misc)
# for a given trip name from the 'prices' table.
def get_price_breakdown_by_trip_name(trip_name):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        SELECT Travelto, Travelthere, Food, Housing, School, Misc
        FROM prices
        WHERE location = %s
        """
        cursor.execute(query, (trip_name,))
        row = cursor.fetchone()
        return True, row if row else []
    except Exception as e:
        return False, str(e)

# Establishes and returns a MySQL connection using credentials from the config file.
# Logs and handles any connection errors.
def create_connection():
    """Establishes and returns a MySQL connection using credentials from the config file."""
    import config as myconfig
    config = myconfig.Config.dbinfo().copy()
    
    try:
        # First ensure database exists
        if not create_database_if_not_exists(config):
            print("Failed to create database")
            return None
            
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

# Return a MySQL connection object using the provided config (for pytest)
def get_connection(config):
    return mysql.connector.Connect(**config)

# Checks if a user with the given username and password exists in the userProfile table.
def authenticate_user(username, password):
    conn = create_connection()
    if conn is None:
        return False
        
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM userProfile WHERE userName = %s AND passwordHash = %s", (username, password))
        user = cursor.fetchone()
        return user is not None
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return False
    finally:
        if conn:
            conn.close()
