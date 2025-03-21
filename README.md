# Penny Pilot

Penny Pilot is a financial planning tool designed to help students at Northern Arizona University (NAU) manage their budget and savings for studying abroad. Many students struggle with financial planning, which discourages them from pursuing international education opportunities. Penny Pilot provides a user-friendly platform to track expenses, set savings goals, and visualize financial progress, reducing stress and empowering students to focus on learning.

## Getting Started

These instructions will help you set up the Penny Pilot application on your local machine for development and testing.

### Prerequisites

To run this project, ensure you have the following installed:
- Python (Latest Version)
- MySQL Database Server
- Git (for version control)

### Installing

#### Mac Installation

1. **Install Homebrew** (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **Install Python 3** (if not already installed):
```bash
brew install python3
```

3. **Install MySQL**:
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

4. **Clone the repository**:
```bash
git clone https://github.com/sesartrumpet/cs386-pennypilot.git
cd cs386-pennypilot
```

5. **Create and activate virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate
```

6. **Install dependencies**:
```bash
pip install -r requirements.txt
```

7. **Configure MySQL Database**:
```bash
mysql -u root -p
```
Then in the MySQL prompt:
```sql
CREATE DATABASE pennyPilot;
```

8. **Run the application**:
```bash
python3 main.py
```

#### Windows Installation

1. **Install Python**:
   - Download Python from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"

2. **Install MySQL**:
   - Download MySQL Installer from [mysql.com](https://dev.mysql.com/downloads/installer/)
   - Run the installer and follow the setup wizard
   - Remember your root password

3. **Clone the repository**:
```bash
git clone https://github.com/sesartrumpet/cs386-pennypilot.git
cd cs386-pennypilot
```

4. **Create and activate virtual environment**:
```bash
python -m venv venv
.\venv\Scripts\activate
```

5. **Install dependencies**:
```bash
pip install mysql-connector-python
```

6. **Configure MySQL Database**:
```bash
mysql -u root -p
```
Then in the MySQL prompt:
```sql
CREATE DATABASE pennyPilot;
```

7. **Run the application**:
```bash
python main.py
```

### Troubleshooting

#### Mac
- If pip installation fails with "externally-managed-environment" error, make sure to use the virtual environment
- If MySQL connection fails, verify MySQL service is running: `brew services list`
- If permission errors occur, you may need to use `sudo` for some commands

#### Windows
- If 'python' is not recognized, try 'py' instead
- If MySQL is not recognized as a command, add MySQL to your system's PATH
- If virtual environment activation fails, ensure you're using the correct path separator (\)

## Deployment

## Running the Tests

```bash
pytest
```

This will run unit tests covering key functionalities such as:
- Adding expenses and income data
- Budget visualization rendering
- User authentication workflow

## Built With

* [Python](https://www.python.org/) - Backend language
* [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework
* [MySQL](https://www.mysql.com/) - Database for storing user budgeting data

## Contributing

Please read [CONTRIBUTING.md](https://github.com/sesartrumpet/cs386-pennypilot/blob/main/CONTRIBUTING.md) for details on our code of conduct and how to submit pull requests.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For available versions, see the [tags on this repository](https://github.com/sesartrumpet/cs386-pennypilot/tags).

## Authors

* **Victor Rodriguez**
* **Sesar Parra**
* **Elijah Sprouse**
* **Manjot Kaur**
* **Kyle Radzvin**
* **Vikram Singh**

See the list of [contributors](https://github.com/sesartrumpet/cs386-pennypilot/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* Special thanks to NAU faculty and advisors for guidance.
* Inspiration from existing financial planning tools.
* Hat tip to open-source contributors whose code was used.

