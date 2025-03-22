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
    run_sql_file(cursor, 'data.sql')
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
