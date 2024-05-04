def create_tables():

    # Table for a specific ticket with a ID as key
    CREATE_TICKET_TABLE = """
        CREATE TABLE IF NOT EXIST ticket(
            ticketID INT AUTO_INCREMENT PRIMARY KEY,
            destination VARCHAR(255) NOT NULL,
            price INT NOT NULL,
            numberOf INT NOT NULL
        )
    """

    # Table for peoples
    CREATE_PEOPLE_TABLE = """
        CREATE TABLE IF NOT EXIST people(
            threshold INT NOT NULL, 
            speed INT NOT NULL,
            location VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            funds INT NOT NULL,
            people_ticketID INT,
            FOREIGN KEY (people_ticketID) REFERENCES ticket(ticketID)
            UNIQUE KEY (ticketID)
        )
    """

    # One specific trainstaion
    CREATE_TRAIN_TABLE = """
        CREATE TABLE IF NOT EXIST train(
            ID INT AUTO_INCREMENT PRIMARY KEY,
            location VARCHAR(255) NOT NULL,
            available BOOL NOT NULL,
        )
        """
    
    # One specific bus-station
    CREATE_BUS_TABLE = """
        CREATE TABLE IF NOT EXIST bus(
            ID INT AUTO_INCREMENT PRIMARY KEY,
            location VARCHAR(255) NOT NULL,
            available BOOL NOT NULL,
        )
        """
    
    # Time table  
    CREATE_SCHEDULE_TABLE = """
        CREATE TABLE IF NOT EXIST schedule(
            depature_time DATETIME NOT NULL,
            arrival_time DATETIME NOT NULL, 
            total VARCHAR(255) NOT NULL, 
            end_station VARCHAR(255) NOT NULL,
        )
        """