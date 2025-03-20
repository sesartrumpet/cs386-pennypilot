# Penny Pilot

Penny Pilot is a financial planning tool designed to help students at Northern Arizona University (NAU) manage their budget and savings for studying abroad. Many students struggle with financial planning, which discourages them from pursuing international education opportunities. Penny Pilot provides a user-friendly platform to track expenses, set savings goals, and visualize financial progress, reducing stress and empowering students to focus on learning.

## Getting Started

These instructions will help you set up the Penny Pilot application on your local machine for development and testing. See the deployment section for notes on how to deploy this project to a live system.

### Prerequisites

To run this project, ensure you have the following installed:

```
- Python (Latest Version)
- MySQL Database Server
- Tkinter (comes with Python standard library)
- Git (for version control)
```

### Installing

Follow these steps to set up the development environment:

1. Clone the repository:
```
git clone https://github.com/sesartrumpet/cs386-pennypilot.git
cd cs386-pennypilot
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Configure MySQL Database:
   - Create a new database `penny_pilot`
   - Update database credentials in the application config file

4. Run the application:
```
python main.py
```

End with an example of how users can add sample financial data and visualize their savings progress.

## Running the Tests

### Break down into end-to-end tests

The testing framework ensures all functionalities work as expected.

```
pytest
```

This will run unit tests covering key functionalities such as:
- Adding expenses and income data
- Budget visualization rendering
- User authentication workflow

### Coding Style Tests

To maintain code quality, run the linter:
```
pylint main.py
```

## Deployment

To deploy Penny Pilot to a live system:

- TBD

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

