def create_tables():

    CREATE_TICKET_TABLE = """
        CREATE TABLE IF NOT EXIST ticket(
            ticketID INT AUTO_INCREMENT PRIMARY KEY,
            destination VARCHAR(255) NOT NULL,
            price INT NOT NULL,
            numberOf INT NOT NULL
        )
"""