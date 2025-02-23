# PennyPilot

## Prerequisites

- Git - Install [here](https://git-scm.com/downloads)
- Python (>=3.8) - Install [here](https://www.python.org/downloads/)
- MySQL - Install [here](https://dev.mysql.com/downloads/)

## Setting Up

**Note:** This project is still in progress as we transition from C to Python. This README will be updated accordingly.

1. **Create an empty folder named `pennypilot`.**

2. **Initialize Git and link to the repository**
    
    Open a terminal in the `pennypilot` folder and run:
    
    ```sh
    git init
    git remote add origin https://github.com/sesartrumpet/cs386-pennypilot.git
    git pull origin main
    ```

3. **Install dependencies**
    
    Since dependencies are still being determined due to transitioning from C to Python, install necessary packages as needed using:
    
    ```sh
    pip install <package-name>
    ```

    Once dependencies are finalized, they should be added to a `requirements.txt` file.

4. **Set up the MySQL database**
    
    Ensure MySQL is running and create a database for the project:
    
    ```sql
    CREATE DATABASE pennypilot_db;
    ```
    
    Configure the database connection settings in the project as needed.
    
5. **Run the application**
    
    ```sh
    python app.py
    ```
    
    The application should now be running. Open `http://127.0.0.1:5000/` in your web browser to view it.

**This document will be updated as the project evolves.**