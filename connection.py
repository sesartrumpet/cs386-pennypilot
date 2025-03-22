# import MySQL connector driver manager
import mysql.connector


# main program
def main(config):
    # open the database connection
    connector = mysql.connector.Connect(**config)
    # check if the connection is open
    print("Is connected?", connector.is_connected())
    # print the server's version
    print("MySQL Server version:", connector.get_server_info())


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
