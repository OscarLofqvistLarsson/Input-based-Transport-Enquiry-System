from connection import *
from tables import *
from datetime import datetime, timedelta

# bus
def populate_bus():
    locations = ["Ronneby","Listerby","Lyckeby","Karlskrona", "Karlshamn", "Sölvesborg", "Bräkne-Hoby", "Jämjö","Nättraby", "Mörrum"]
    IDs = ["b1","b2","b3","b4","b5","b6","b7","b8","b9","b10"]

    db_connection = establish_db_connection()

    if db_connection:

        db_cursor = db_connection.cursor()

        insert_bus = """
        INSERT INTO bus (ID, location)
        VALUES(%s, %s)
        """
        for x in range(len(locations)):

            db_cursor.execute(insert_bus, (IDs[x], locations[x]))

        db_connection.commit()

        close_db_connection(db_connection)

    print("Bus table has been populated")

# train
def populate_train():

    locations = [ "Sölvesborg","Karlshamn","Bräkne-Hoby","Ronneby","Bergåsa", "Karlskrona",]
    IDs = ["t1","t2","t3","t4","t5","t6"]

    db_connection = establish_db_connection()

    if db_connection:

        db_cursor = db_connection.cursor()

        insert_trains = """
        INSERT INTO train (ID,location)
        VALUES(%s, %s)
        """
        for x in range(len(locations)):
            available = True

            db_cursor.execute(insert_trains, (IDs[x], locations[x]))

        db_connection.commit()

        close_db_connection(db_connection)

    print("Train table has been populated")


# schedule
def populate_train_schedule():
    locations = ["Sölvesborg", "Karlshamn", "Bräkne-Hoby", "Ronneby", "Bergåsa", "Karlskrona"]
    start_time = datetime.strptime("06:00:00", "%H:%M:%S")
    end_time = datetime.strptime("22:00:00", "%H:%M:%S")
    travel_time = timedelta(minutes=10)

    schedule = []

    current_time = start_time
    while current_time < end_time:
        # Going from Sölvesborg to Karlskrona
        for i in range(len(locations) - 1):
            start_station = locations[i]
            end_station = locations[i + 1]
            arrival_time = current_time + travel_time

            schedule.append((current_time.strftime("%H:%M:%S"), arrival_time.strftime("%H:%M:%S"),
                            str(travel_time), start_station, end_station))

            current_time = arrival_time

        # Going back to Sölvesborg
        for i in range(len(locations) - 1, 0, -1):
            start_station = locations[i]
            end_station = locations[i - 1]
            arrival_time = current_time + travel_time

            schedule.append((current_time.strftime("%H:%M:%S"), arrival_time.strftime("%H:%M:%S"),
                            str(travel_time), start_station, end_station))

            current_time = arrival_time

    # Adding another train starting from Karlskrona and going in the opposite direction
    current_time = start_time
    while current_time < end_time:
        # Going from Karlskrona to Sölvesborg
        for i in range(len(locations) - 1, 0, -1):
            start_station = locations[i]
            end_station = locations[i - 1]
            arrival_time = current_time + travel_time

            schedule.append((current_time.strftime("%H:%M:%S"), arrival_time.strftime("%H:%M:%S"), 
                            str(travel_time), start_station, end_station))

            current_time = arrival_time


        # Going back to Karlskrona
        for i in range(len(locations) - 1):
            start_station = locations[i]
            end_station = locations[i + 1]
            arrival_time = current_time + travel_time

            schedule.append((current_time.strftime("%H:%M:%S"), arrival_time.strftime("%H:%M:%S"), 
                            str(travel_time), start_station, end_station))

            current_time = arrival_time

    db_connection = establish_db_connection()

    if db_connection:

        db_cursor = db_connection.cursor()

        insert_query = "INSERT INTO train_schedule (departure_time, arrival_time, total, start_station, end_station) VALUES (%s, %s, %s, %s, %s)"

        for entry in schedule:
            departure_time, arrival_time, total, start_station, end_station = entry
            values = (departure_time, arrival_time, total, start_station, end_station)
            db_cursor.execute(insert_query, values)

        db_connection.commit()

        close_db_connection(db_connection)

    print("Train schedule have been populated")


def populate_bus_schedule():
    locations = ["Sölvesborg",  "Mörrum", "Karlshamn", "Bräkne-Hoby", "Ronneby","Listerby","Nättraby", "Karlskrona",  "Lyckeby", "Jämjö", ]
    start_time = datetime.strptime("06:00:00", "%H:%M:%S")
    end_time = datetime.strptime("22:00:00", "%H:%M:%S")
    delta_time = timedelta(minutes=12)
    travel_time = timedelta(minutes=12)

    schedule = []

    current_time = start_time
    while current_time < end_time:
        # Going from Sölvesborg to jämjö
        for i in range(len(locations) - 1):
            start_station = locations[i]
            end_station = locations[i + 1]
            arrival_time = current_time + travel_time

            schedule.append((current_time.strftime("%H:%M:%S"), arrival_time.strftime("%H:%M:%S"),
                            str(travel_time), start_station, end_station))

            current_time = arrival_time

        # Going back to Sölvesborg
        for i in range(len(locations) - 1, 0, -1):
            start_station = locations[i]
            end_station = locations[i - 1]
            arrival_time = current_time + travel_time

            schedule.append((current_time.strftime("%H:%M:%S"), arrival_time.strftime("%H:%M:%S"),
                            str(travel_time), start_station, end_station))

            current_time = arrival_time

    # Adding another bus starting from jämjö and going in the opposite direction
    current_time = start_time
    while current_time < end_time:
        # Going from jämjö to Sölvesborg
        for i in range(len(locations) - 1, 0, -1):
            start_station = locations[i]
            end_station = locations[i - 1]
            arrival_time = current_time + travel_time

            schedule.append((current_time.strftime("%H:%M:%S"), arrival_time.strftime("%H:%M:%S"),
                            str(travel_time), start_station, end_station))

            current_time = arrival_time
        # Going back to Karlskrona
        for i in range(len(locations) - 1):
            start_station = locations[i]
            end_station = locations[i + 1]
            arrival_time = current_time + travel_time

            schedule.append((current_time.strftime("%H:%M:%S"), arrival_time.strftime("%H:%M:%S"),
                            str(travel_time), start_station, end_station))

            current_time = arrival_time


    db_connection = establish_db_connection()

    if db_connection:

        db_cursor = db_connection.cursor()

        insert_query = "INSERT INTO bus_schedule (departure_time, arrival_time, total, start_station, end_station) VALUES (%s, %s, %s, %s, %s)"

        for entry in schedule:
            depature_time, arrival_time, total, start_station, end_station = entry
            values = (depature_time, arrival_time, total, start_station, end_station)
            db_cursor.execute(insert_query, values)

        db_connection.commit()

        close_db_connection(db_connection)

    print("Bus schedule have been populated")


if __name__ == "__main__":
    populate_train()
    populate_bus()
    populate_train_schedule()
    populate_bus_schedule()