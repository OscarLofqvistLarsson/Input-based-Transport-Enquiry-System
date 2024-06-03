from connection import *

def create_tables():
    # Table for people
    CREATE_PEOPLE_TABLE = """
        CREATE TABLE IF NOT EXISTS people(
            fname VARCHAR(20) NOT NULL PRIMARY KEY,
            funds INT NOT NULL,
            people_ticket_id INT AUTO_INCREMENT NOT NULL,
            UNIQUE KEY (people_ticket_id)
        )
    """

    # Table for a specific ticket with an ID as the key
    CREATE_TICKET_TABLE = """
        CREATE TABLE IF NOT EXISTS ticket(
            ticketID INT AUTO_INCREMENT PRIMARY KEY,
            location VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            price INT NOT NULL,
            people_ticket_id INT NOT NULL,
            FOREIGN KEY (people_ticket_id) REFERENCES people(people_ticket_id)
        )
    """

    # One specific train-station
    CREATE_TRAIN_TABLE = """
        CREATE TABLE IF NOT EXISTS train(
            ID VARCHAR(255) PRIMARY KEY,
            location VARCHAR(255) NOT NULL
        )
    """

    # One specific bus-station
    CREATE_BUS_TABLE = """
        CREATE TABLE IF NOT EXISTS bus(
            ID VARCHAR(255) PRIMARY KEY,
            location VARCHAR(255) NOT NULL
        )
    """

    # Train timetable
    CREATE_TRAIN_SCHEDULE_TABLE = """
        CREATE TABLE IF NOT EXISTS train_schedule(
            departure_time TIME NOT NULL,
            arrival_time TIME NOT NULL,
            total VARCHAR(255) NOT NULL,
            start_station VARCHAR(255) NOT NULL,
            end_station VARCHAR(255) NOT NULL
        )
    """

    # Bus timetable
    CREATE_BUS_SCHEDULE_TABLE = """
        CREATE TABLE IF NOT EXISTS bus_schedule(
            departure_time TIME NOT NULL,
            arrival_time TIME NOT NULL,
            total VARCHAR(255) NOT NULL,
            start_station VARCHAR(255) NOT NULL,
            end_station VARCHAR(255) NOT NULL
        )
    """

    # Preference table
    CREATE_PREFERENCE_TABLE = """
        CREATE TABLE IF NOT EXISTS preference(
            fname VARCHAR(20) NOT NULL,
            train BOOL,
            bus BOOL,
            FOREIGN KEY (fname) REFERENCES people(fname)
        )
    """

    db_connection = establish_db_connection()

    if db_connection:
        db_cursor = db_connection.cursor()
        db_cursor.execute(CREATE_PEOPLE_TABLE)
        db_cursor.execute(CREATE_TICKET_TABLE)
        db_cursor.execute(CREATE_TRAIN_TABLE)
        db_cursor.execute(CREATE_BUS_TABLE)
        db_cursor.execute(CREATE_TRAIN_SCHEDULE_TABLE)
        db_cursor.execute(CREATE_BUS_SCHEDULE_TABLE)
        db_cursor.execute(CREATE_PREFERENCE_TABLE)

        db_connection.commit()

        print("Database has been initialized")

        close_db_connection(db_connection)
    else:
        print("Connection to database failed")

if __name__ == "__main__":
    create_tables()
