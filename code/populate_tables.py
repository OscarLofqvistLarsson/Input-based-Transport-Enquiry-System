from connection import *
from tables import *

# bus
def populate_bus():
    locations = ["Ronneby","Listerby","Lyckeby","Karlskrona", "Karlshamn", "Sölvesborg", "Bräkne-Hoby", "Jämjö","Nättraby", "Mörrum"]
    IDs = ["b1","b2","b3","b4","b5","b6","b7","b8","b9","b10"]

    db_connection = establish_db_connection()

    if db_connection:

        db_cursor = db_connection.cursor()

        insert_bus = """
        INSERT INTO bus (ID, location, available)
        VALUES(%s, %s, %s)
        """
        for x in range(len(locations)):
            available = True

            db_cursor.execute(insert_bus, (IDs[x], locations[x], available))

        db_connection.commit()

        close_db_connection(db_connection)

    print("Bus table has been populated")



# train
def populate_train():

    locations = ["Ronneby", "Karlskrona", "Karlshamn", "Sölvesborg", "Bräkne-Hoby"]
    IDs = ["t1","t2","t3","t4","t5"]

    db_connection = establish_db_connection()

    if db_connection:

        db_cursor = db_connection.cursor()

        insert_trains = """
        INSERT INTO train (ID,location, available)
        VALUES(%s, %s, %s)
        """
        for x in range(len(locations)):
            available = True

            db_cursor.execute(insert_trains, (IDs[x], locations[x], available))

        db_connection.commit()

        close_db_connection(db_connection)

    print("Train table has been populated")


# schedule



if __name__ == "__main__":
    populate_train()
    populate_bus()