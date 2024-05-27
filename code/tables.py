from connection import *

def create_tables():

    # Table for a specific ticket with a ID as key
    CREATE_TICKET_TABLE = """
        CREATE TABLE IF NOT EXISTS ticket(
            ticketID INT AUTO_INCREMENT PRIMARY KEY,
            location VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            price INT NOT NULL
        )
    """

    # Table for peoples
    CREATE_PEOPLE_TABLE = """
        CREATE TABLE IF NOT EXISTS people(
            fname varchar (20) NOT NULL,
            threshold char(3) NOT NULL,
            funds INT NOT NULL,
            people_ticketID INT,
            FOREIGN KEY (people_ticketID) REFERENCES ticket(ticketID),
            UNIQUE KEY (people_ticketID)
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

    # Train time table
    CREATE_TRAIN_SCHEDULE_TABLE = """
        CREATE TABLE IF NOT EXISTS train_schedule(
            departure_time TIME NOT NULL,
            arrival_time TIME NOT NULL,
            total VARCHAR(255) NOT NULL,
            start_station VARCHAR(255) NOT NULL,
            end_station VARCHAR(255) NOT NULL
        )
    """
    # Bus time table
    CREATE_BUS_SCHEDULE_TABLE = """
        CREATE TABLE IF NOT EXISTS bus_schedule(
            departure_time TIME NOT NULL,
            arrival_time TIME NOT NULL,
            total VARCHAR(255) NOT NULL,
            start_station VARCHAR(255) NOT NULL,
            end_station VARCHAR(255) NOT NULL
        )
    """
    db_connection = establish_db_connection()

    if db_connection:

        db_cursor = db_connection.cursor()

        db_cursor.execute(CREATE_BUS_TABLE)
        db_cursor.execute(CREATE_TRAIN_SCHEDULE_TABLE)
        db_cursor.execute(CREATE_BUS_SCHEDULE_TABLE)
        db_cursor.execute(CREATE_TICKET_TABLE)
        db_cursor.execute(CREATE_PEOPLE_TABLE)
        db_cursor.execute(CREATE_TRAIN_TABLE)

        db_connection.commit()

        print("Database have been initialized")

        close_db_connection(db_connection)
    else:
        print("connection to database failed")


if __name__ == "__main__":
    create_tables()