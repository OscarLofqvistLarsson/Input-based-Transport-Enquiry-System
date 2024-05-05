from connection import *
from tables import *

# bus
def populate_bus():

    CREATE_BUS_TRIGGER = """
            CREATE TRIGGER add_to_id_bus
            BEFORE INSERT ON bus
            FOR EACH ROW 
            BEGIN
                SET NEW.ID = CONCAT('b', CAST(NEW.ID AS CHAR));
            END;
    """



    locations = ["Ronneby","Listerby","Lyckeby","Karlskrona", "Karlshamn", "Sölvesborg", "Bräkne-Hoby", "Jämjö","Nättraby", "Mörrum"]

    db_connection = establish_db_connection()

    if db_connection:

        db_cursor = db_connection.cursor()

        insert_bus = """
        INSERT INTO bus (location, available)
        VALUES(%s, %s)
        """
        for location in locations:
            available = True

            db_cursor.execute(insert_bus, (location, available))

        db_connection.commit()

        close_db_connection(db_connection)

    print("Bus table has been populated")





# train
def populate_train():

    CREATE_BUS_TRIGGER = """
        CREATE TRIGGER add_to_id_train
        BEFORE INSERT ON train
        FOR EACH ROW 
        BEGIN
            SET NEW.ID = CONCAT('t', CAST(NEW.ID AS CHAR));
        END;
    """

    locations = ["Ronneby", "Karlskrona", "Karlshamn", "Sölvesborg", "Bräkne-Hoby"]

    db_connection = establish_db_connection()

    if db_connection:

        db_cursor = db_connection.cursor()

        insert_trains = """
        INSERT INTO train (location, available)
        VALUES(%s, %s)
        """
        for location in locations:
            available = True

            db_cursor.execute(insert_trains, (location, available))

        db_connection.commit()

        close_db_connection(db_connection)

    print("Train table has been populated")


# schedule



if __name__ == "__main__":
    populate_train()
    populate_bus()