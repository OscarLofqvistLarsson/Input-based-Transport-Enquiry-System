def create_tables():

    CREATE_TICKET_TABLE = """
        CREATE TABLE IF NOT EXIST ticket(
            ticketID INT AUTO_INCREMENT PRIMARY KEY,
            destination VARCHAR(255) NOT NULL,
            price INT NOT NULL,
            numberOf INT NOT NULL
        )
    """
    CREATE_PEOPLE_TABLE = """
        CREATE TABLE IF NOT EXIST people(
            threshold INT NOT NULL,
            speed INT NOT NULL,
            location VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            funds INT NOT NULL,
            ticketID INT,
            FOREIGN KEY (ticketID) REFERENCES ticket(ticketID)
            UNIQUE KEY (ticketID)
        )
    """

    CREATE_TRAIN_TABLE = """
        CREATE TABLE IF NOT EXIST train(
            ID INT AUTO_INCREMENT PRIMARY KEY,
            schedule #hur skulle denna fungera?
        )
        """"Bitch"""""
        """