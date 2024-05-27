# Public Transport Ticket Booking System

## Description
This Python program allows users to book tickets for public transport (trains and buses), view schedules, and check personal information related to their bookings. It interacts with a MySQL database to store and retrieve data.

## Files
- **connection.py**: Contains functions to establish and close connections to the MySQL database.
- **tables.py**: Contains SQL queries to create database tables.
- **populate_tables.py**: Contains functions to populate the database tables with initial data.
- **main.py**: Main program file where the core functionality is implemented.

## Dependencies
- MySQL Connector Python: Used to connect Python to MySQL databases.
- ReportLab: Used to generate PDF files for train and bus schedules.

## How to Run
1. Install the necessary dependencies using `pip install mysql-connector-python reportlab`.
2. Set up a MySQL database and configure the connection details in `connection.py`.
3. Run `python tables.py` to create tables.
4. Run `python populate_tables.py` to populate the database tables.
5. INSERT necessary `SQL - files` into you database
6. Run `python main.py` to start the program.


## Usage
- Upon running the program, users are prompted to choose between buying a ticket, viewing the current schedule, or checking personal information.
- To buy a ticket, users need to provide their name, current station, destination, preference (train/bus), and available funds.
- To view the schedule, users can choose between trains and buses and a PDF with the schedule will be generated.
- To check personal information, users need to provide their name, and details such as remaining funds and booked tickets will be displayed.

## Contributors
- [Your Name]

## License
This project is licensed under the [MIT License](LICENSE).
