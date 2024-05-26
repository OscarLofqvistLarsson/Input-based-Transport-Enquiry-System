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

    locations = [ "Sölvesborg","Karlshamn","Bräkne-Hoby","Ronneby","Bergåsa", "Karlskrona",]
    IDs = ["t1","t2","t3","t4","t5","t6"]

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


def purchase_ticket(person_name, start_location, end_location, ticket_price, number_of_tickets, transport_type):
    db_connection = establish_db_connection()

    if db_connection:
        db_cursor = db_connection.cursor()

        # Insert ticket into ticket table
        insert_ticket_query = """
        INSERT INTO ticket (destination, price, numberOf)
        VALUES (%s, %s, %s)
        """
        db_cursor.execute(insert_ticket_query, (end_location, ticket_price, number_of_tickets))
        ticket_id = db_cursor.lastrowid  # Get the last inserted ticketID

        # Insert person into people table
        insert_people_query = """
        INSERT INTO people (threshold, location, destination, funds, people_ticketID)
        VALUES (%s, %s, %s, %s, %s)
        """
        threshold = 0  # Assuming threshold is 0 for this example
        funds = 0      # Assuming funds are 0 for this example

        db_cursor.execute(insert_people_query, (threshold, start_location, end_location, funds, ticket_id))

        db_connection.commit()

        close_db_connection(db_connection)

        print(f"Ticket purchased for {person_name} from {start_location} to {end_location}.")
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":

    choice = input("Would you like to buy a ticket or see the current schedule?\n")
    if choice == "ticket":
        person_location = input("At what station are you at the moment?\n")
        person_destination = input("Where are you planning on heading today?\n")
        threshold = input("Specify preference for train or bus by either entering t1-t10 or b1-b10 respectively\n")
        funds = int(input("How much money do you have for your traveling needs?\n"))

        result = estimated_ticket(person_location, person_destination, threshold, funds) # Estimated ticket ska ställa en fråga om man vill köpa den, inte tillagt
        print(result)
    elif choice == "schedule":

        try:
            os.remove("train_schedule.pdf")
            os.remove("bus_schedule.pdf")
        except:
            FileNotFoundError

        schedule_pdf()

