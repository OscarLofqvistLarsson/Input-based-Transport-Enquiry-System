from connection import *
from tables import *
from populate_tables import *
from datetime import datetime, timedelta

# List of stations in order
locations_train = ["Sölvesborg", "Karlshamn", "Bräkne-Hoby", "Ronneby", "Bergåsa", "Karlskrona"]
locations_bus = ["Sölvesborg",  "Mörrum", "Karlshamn", "Bräkne-Hoby", "Ronneby","Listerby","Nättraby", "Karlskrona",  "Lyckeby", "Jämjö", ]

def check_time_diff(db_cursor, person_location, current_time, person_destination):
    def get_next_departure_time(transport_type, person_location, current_time):
        query = f"""
        SELECT departure_time, end_station
        FROM {transport_type}_schedule
        WHERE start_station = %s AND departure_time >= %s
        ORDER BY departure_time
        LIMIT 1
        """
        db_cursor.execute(query, (person_location, current_time.time()))
        result = db_cursor.fetchone()
        if result:
            departure_time, end_station = result
            departure_time = datetime.strptime(str(departure_time), "%H:%M:%S").time()
            departure_datetime = datetime.combine(current_time.date(), departure_time)
            if departure_datetime < current_time:
                departure_datetime += timedelta(days=1)
            return departure_datetime, end_station
        return None, None

    train_departure, train_end_station = get_next_departure_time('train', person_location, current_time)
    bus_departure, bus_end_station = get_next_departure_time('bus', person_location, current_time)

    if train_departure is None and bus_departure is None:
        return None

def estimated_ticket(fname, person_location, person_destination, funds):
    global ticket_price
    ticket_price = 0

    db_connection = establish_db_connection()
    if db_connection:
        db_cursor = db_connection.cursor()

        arg = (f'{fname}',)
        db_cursor.callproc('GetPreferences', arg)

        for result in db_cursor.stored_results():
            fetched_result = result.fetchone()

            return fetched_result
    else:
        return "Input for preference needs to start with t or b for train or bus"

    current_datetime = datetime.now().replace(microsecond=0)


    def find_next_station(db_cursor, transport_type, current_station, travel_time, visited_stations):
        query_schedule = """
        SELECT CAST(departure_time AS CHAR) AS departure_time, CAST(arrival_time AS CHAR) AS arrival_time, start_station, end_station, total
        FROM {}_schedule
        WHERE start_station = %s AND departure_time >= %s
        ORDER BY departure_time
        LIMIT 1
        """.format(transport_type)

        db_cursor.execute(query_schedule, (current_station, travel_time))
        for station in db_cursor.fetchall():
            _, _, _, end_station, _ = station
            if end_station not in visited_stations:
                return station
        return None

    # Check for misspell
    if person_location not in locations_train and person_location not in locations_bus:
        return f"Error: The station '{person_location}' is not a valid station."
    if person_destination not in locations_train and person_destination not in locations_bus:
        return f"Error: The station '{person_destination}' is not a valid station."

    db_connection = establish_db_connection()
    if db_connection:
        db_cursor = db_connection.cursor()
        total_travel_time = timedelta()
        current_station = person_location
        travel_map = []
        visited_stations = set()
        transport_type, next_departure = check_time_diff(db_cursor, person_location, current_datetime, person_destination, locations_train if fetched_result[1] == 1 else locations_bus)
        if not transport_type:
            return "No available transport matches the criteria."

        while current_station != person_destination:
            visited_stations.add(current_station)
            find_station = find_next_station(db_cursor, transport_type, current_station, current_datetime, visited_stations)
            if not find_station:
                return "No bus or train match the criteria, check that your spelling is correct."

            departure_time_str, arrival_time_str, start_station, end_station, total = find_station

            departure_time = datetime.strptime(departure_time_str, "%H:%M:%S").time()
            arrival_time = datetime.strptime(arrival_time_str, "%H:%M:%S").time()

            departure_datetime = datetime.combine(current_datetime.date(), departure_time)
            arrival_datetime = datetime.combine(current_datetime.date(), arrival_time)

            if arrival_datetime < departure_datetime:
                arrival_datetime += timedelta(days=1)

            segment_travel_time = arrival_datetime - departure_datetime
            total_travel_time += segment_travel_time
            travel_map.append((departure_time_str, arrival_time_str, start_station, end_station, total))

            current_datetime = arrival_datetime

            # Check if the direction is correct
            if transport_type == 'train':
                current_index = locations_train.index(current_station)
                next_index = locations_train.index(end_station)
                final_index = locations_train.index(person_destination)

            else:
                current_index = locations_bus.index(current_station)
                next_index = locations_bus.index(end_station)
                final_index = locations_bus.index(person_destination)

            if (next_index > current_index and final_index > current_index) or (next_index < current_index and final_index < current_index):
                current_station = end_station
            else:
                # If the immediate next station is not in the direction, continue to look for other options.
                alternative_station_found = False
                for station in locations_train[current_index + 1:]:
                    if station not in visited_stations:
                        find_station = find_next_station(db_cursor, transport_type, current_station, current_datetime, visited_stations)
                        if find_station:
                            current_station = end_station
                            alternative_station_found = True
                            break
                if not alternative_station_found:
                    return "No direct route towards the destination found."
            ticket_price += 50
            transport_type, next_departure = check_time_diff(db_cursor, current_station, current_datetime, person_destination, locations_train if transport_type == 'train' else locations_bus)
            if not transport_type:
                return "No available transport matches the criteria."

        total_minutes = total_travel_time.total_seconds() / 60

        if funds >= ticket_price:
            result = "Travel itinerary:\n"
            for departure_time_str, arrival_time_str, start_station, end_station, total in travel_map:
                result += f"From {start_station} to {end_station}, departure at {departure_time_str}, arrival at {arrival_time_str}\n"
            result += f"Total travel time: {total_minutes} minutes\n"
            result += f"Ticket price: {ticket_price}\n"
            return result
        else:
            return "Insufficient funds for the ticket."
    else:
        return "Connection to database failed"

# Function
def purchase_ticket(location, destination, ticket_price, funds, fname):
    db_connection = establish_db_connection()
    if db_connection:
        db_cursor = db_connection.cursor()

        # Call funktion.sql
        check_ticket_query = """
        SELECT people_ticketID FROM people
        WHERE fname = %s AND people_ticketID IN (
            SELECT ticketID FROM ticket
            WHERE location = %s AND destination = %s AND price = %s
        )
        """
        db_cursor.execute(check_ticket_query, (fname, location, destination, ticket_price))
        existing_ticket = db_cursor.fetchone()

        if existing_ticket:
            print("You already have this ticket.")
            return

        # If the person doesn't have the ticket, proceed with purchase
        check_or_create_ticket_query = """
        SELECT check_or_create_ticket(%s, %s, %s)
        """
        db_cursor.execute(check_or_create_ticket_query, (location, destination, ticket_price))
        ticket_id = db_cursor.fetchone()[0]

        if ticket_id:
            # Insert a record into the people table
            insert_people_query = """
            INSERT INTO people (fname, funds, people_ticket_id, )
            VALUES (%s, %s, %s)
            """
            new_funds = funds - ticket_price
            db_cursor.execute(insert_people_query, (fname,new_funds, ticket_id))

            db_connection.commit()
            close_db_connection(db_connection)

            print(f"Ticket purchased from {location} to {destination}.")
        else:
            print("Failed to create ticket.")
    else:
        print("Failed to connect to the database.")


# Procedure:
def check_name(name):
    db_connection = establish_db_connection()
    if db_connection:
        db_cursor = db_connection.cursor()

        # Prepare the stored procedure call
        call_proc_query = "CALL check_name(%s, @funds)"
        db_cursor.execute(call_proc_query, (name,))

        # Fetch the output parameters
        db_cursor.execute("SELECT @funds")
        result_name = db_cursor.fetchone()

        db_cursor.close()
        close_db_connection(db_connection)

        return result_name
    else:
        return None


def get_person_info(name):
    db_connection = establish_db_connection()
    if db_connection:
        db_cursor = db_connection.cursor()
        query = """
        SELECT person_name, remaining_funds, ticket_start, ticket_destination, ticket_price
        FROM person_ticket_info
        WHERE person_name = %s
        """
        db_cursor.execute(query, (name,))
        person_info = db_cursor.fetchall()
        db_cursor.close()
        close_db_connection(db_connection)

        if person_info:
            print(f"Name: {name}")
            print(f"Remaining Funds: {person_info[-1][1]}") # take the latest row
            print("Tickets:")
            for row in person_info:
                if row[2] and row[3]:  # Check if ticket_start and ticket_destination are not None
                    print(f"  From {row[2]} to {row[3]}, price: {row[4]}")
        else:
            print("No information found for this person.")
    else:
        print("Connection to database failed.")


if __name__ == "__main__":

    while True:
        choice = input("Would you like to buy a ticket, see the current schedule or see information regarding your info?\n")
        if choice == "ticket":
            fname = input("What is your name?\n")
            name_check = check_name(fname)
            if name_check:
                person_location = input("At what station are you at the moment?\n")
                person_destination = input("Where are you planning on heading today?\n")

                funds = name_check[0]
                result = estimated_ticket(fname, person_location, person_destination, funds)
                print(result)

            else:
                person_location = input("At what station are you at the moment?\n")
                person_destination = input("Where are you planning on heading today?\n")
                pref = input("Specify preference for train or bus\n")
                funds = int(input("How much money do you have for your traveling needs?\n"))
                result = estimated_ticket(person_location, person_destination, funds)
                print(result)

            if "Travel itinerary" in result:
                buy_choice = input("Would you like to buy you ticket? ")
                if buy_choice.lower() == "yes":
                    purchase_ticket(person_location ,person_destination, ticket_price, funds,name_tell)

        if choice == "info":
            name_tell = input("What is your name?\n")
            get_person_info(name_tell)

        if choice == "exit":
            print("Exiting program...")
            break