from connection import *
from tables import *
from populate_tables import *
from datetime import datetime, timedelta
from pdf_create import *

# List of stations in order
locations_train = ["Sölvesborg", "Karlshamn", "Bräkne-Hoby", "Ronneby", "Bergåsa", "Karlskrona"]
locations_bus = ["Sölvesborg",  "Mörrum", "Karlshamn", "Bräkne-Hoby", "Ronneby","Listerby","Nättraby", "Karlskrona",  "Lyckeby", "Jämjö"]

def check_time_diff(db_cursor, person_location, current_time, preferences):
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

    if preferences.get('train'):
        train_departure, train_end_station = get_next_departure_time('train', person_location, current_time)
        return 'train', train_departure
    if preferences.get('bus'):
        bus_departure, bus_end_station = get_next_departure_time('bus', person_location, current_time)
        return 'bus', bus_departure

def estimated_ticket(fname, person_location, person_destination, funds, pref):
    db_connection = establish_db_connection()
    if not db_connection:
        return "Connection to database failed"

    db_cursor = db_connection.cursor()

    # Check if the user already exists
    check_user_query = "SELECT fname FROM people WHERE fname = %s"
    db_cursor.execute(check_user_query, (fname,))
    user_exists = db_cursor.fetchone()

    if not user_exists:
        # Insert the new user if they don't exist
        insert_people_query = """
            INSERT INTO people(fname, funds)
            VALUES (%s, %s)
        """
        db_cursor.execute(insert_people_query, (fname, funds))

        if pref == "train":
            pref1 = True
            pref2 = False
        elif pref == "bus":
            pref1 = False
            pref2 = True
        else:
            db_cursor.close()
            close_db_connection(db_connection)
            return "Specify preference as 'train' or 'bus'"

        insert_pref_query = """
            INSERT INTO preference(fname, train, bus)
            VALUES (%s, %s, %s)
        """
        db_cursor.execute(insert_pref_query, (fname, pref1, pref2))

        db_connection.commit()
    else:
        # Retrieve the user's current funds
        get_funds_query = "SELECT funds FROM people WHERE fname = %s"
        db_cursor.execute(get_funds_query, (fname,))
        funds = db_cursor.fetchone()[0]

        # Retrieve the user's preference
        get_pref_query = "SELECT train, bus FROM preference WHERE fname = %s"
        db_cursor.execute(get_pref_query, (fname,))
        pref_result = db_cursor.fetchone()
        if pref_result:
            pref1, pref2 = pref_result
            pref = "train" if pref1 else "bus"

    # Retrieve user preferences for the check_time_diff function
    preferences = {
        'train': pref1,
        'bus': pref2
    }

    current_datetime = datetime.now().replace(microsecond=0)

    def find_next_station(db_cursor, transport_type, current_station, travel_time, visited_stations):
        if transport_type == 'train':
            locations = locations_train
        else:
            locations = locations_bus

        if locations.index(person_location) > locations.index(person_destination):
            direction = -1
        else:
            direction = 1

        query_schedule = f"""
        SELECT CAST(departure_time AS CHAR) AS departure_time, CAST(arrival_time AS CHAR) AS arrival_time, start_station, end_station, total
        FROM {transport_type}_schedule
        WHERE start_station = %s AND departure_time >= %s
        ORDER BY departure_time
        LIMIT 2
        """

        db_cursor.execute(query_schedule, (current_station, travel_time))
        result = db_cursor.fetchall()
        for station in result:
            _, _, _, end_station, _ = station
            if (direction == 1 and locations.index(end_station) > locations.index(current_station)) or \
                (direction == -1 and locations.index(end_station) < locations.index(current_station)):
                if end_station not in visited_stations:
                    return station

    # Check for misspell
    if person_location not in locations_train and person_location not in locations_bus:
        db_cursor.close()
        close_db_connection(db_connection)
        return f"Error: The station '{person_location}' is not a valid station."
    if person_destination not in locations_train and person_destination not in locations_bus:
        db_cursor.close()
        close_db_connection(db_connection)
        return f"Error: The station '{person_destination}' is not a valid station."

    total_travel_time = timedelta()
    current_station = person_location
    travel_map = []
    visited_stations = set()
    transport_type, next_departure = check_time_diff(db_cursor, person_location, current_datetime, preferences)
    if not transport_type:
        db_cursor.close()
        close_db_connection(db_connection)
        return "No available transport matches the criteria."
    global ticket_price
    ticket_price = 0

    while current_station != person_destination:
        visited_stations.add(current_station)
        find_station = find_next_station(db_cursor, transport_type, current_station, current_datetime, visited_stations)
        if not find_station:
            db_cursor.close()
            close_db_connection(db_connection)
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
            for station in (locations_train if transport_type == 'train' else locations_bus)[current_index + 1:]:
                if station not in visited_stations:
                    find_station = find_next_station(db_cursor, transport_type, current_station, current_datetime, visited_stations)
                    if find_station:
                        current_station = end_station
                        alternative_station_found = True
                        break
            if not alternative_station_found:
                db_cursor.close()
                close_db_connection(db_connection)
                return "No direct route towards the destination found."
        ticket_price += 50
        transport_type, next_departure = check_time_diff(db_cursor, current_station, current_datetime, preferences)
        if not transport_type:
            db_cursor.close()
            close_db_connection(db_connection)
            return "No available transport matches the criteria."

    total_minutes = total_travel_time.total_seconds() / 60

    db_cursor.close()
    close_db_connection(db_connection)

    if funds >= ticket_price:
        result = "Travel itinerary:\n"
        for departure_time_str, arrival_time_str, start_station, end_station, total in travel_map:
            result += f"From {start_station} to {end_station}, departure at {departure_time_str}, arrival at {arrival_time_str} \n"
        result += f"Total travel time: {total_minutes} minutes"
        result += f"Ticket price: {ticket_price}"
        return result, ticket_price
    else:
        return "Insufficient funds for the ticket."


def purchase_ticket(location, destination, ticket_price, funds, fname):
    db_connection = establish_db_connection()
    if not db_connection:
        return "Failed to connect to the database."

    db_cursor = db_connection.cursor()

    # Check if the person already has this ticket
    check_ticket_query = """
    SELECT people_ticket_id FROM ticket
    WHERE location = %s AND destination = %s AND price = %s AND people_ticket_id IS NOT NULL
    """
    db_cursor.execute(check_ticket_query, (location, destination, ticket_price))
    existing_ticket = db_cursor.fetchone()

    if existing_ticket:
        db_cursor.close()
        close_db_connection(db_connection)
        return "You already have this ticket."

    # Check or create the ticket
    check_or_create_ticket_query = """
    SELECT check_or_create_ticket(%s, %s, %s)
    """
    db_cursor.execute(check_or_create_ticket_query, (location, destination, ticket_price))
    ticket_id = db_cursor.fetchone()[0]

    if ticket_id:
        # Update the person's funds
        update_funds_query = """
        UPDATE people
        SET funds = %s
        WHERE fname = %s
        """
        new_funds = funds - ticket_price
        db_cursor.execute(update_funds_query, (new_funds, fname))

        # Associate the ticket with the person
        associate_ticket_query = """
        UPDATE ticket
        SET people_ticket_id = (
            SELECT people_ticket_id FROM people WHERE fname = %s
        )
        WHERE ticketID = %s
        """
        db_cursor.execute(associate_ticket_query, (fname, ticket_id))

        db_connection.commit()
        db_cursor.close()
        close_db_connection(db_connection)

        return f"Ticket purchased from {location} to {destination}."
    else:
        db_cursor.close()
        close_db_connection(db_connection)
        return "Failed to create ticket."

def get_person_info(name):
    db_connection = establish_db_connection()
    if not db_connection:
        return "Connection to database failed."

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


if __name__ == "__main__":
    while True:
        choice = input("Would you like to buy a ticket, see the current schedule, or see information regarding your info?\n").strip().lower()

        if choice == "ticket":
            fname = input("What is your name?\n").strip()
            person_location = input("At what station are you at the moment?\n").strip()
            person_destination = input("Where are you planning on heading today?\n").strip()

            db_connection = establish_db_connection()
            if db_connection:
                db_cursor = db_connection.cursor()
                check_funds_query = "SELECT funds FROM people WHERE fname = %s"
                db_cursor.execute(check_funds_query, (fname,))
                result = db_cursor.fetchone()

                if result:
                    funds = result[0]
                else:
                    funds = int(input("How much money do you have?\n"))

                check_pref_query = "SELECT train, bus FROM preference WHERE fname = %s"
                db_cursor.execute(check_pref_query, (fname,))
                result = db_cursor.fetchone()
                if result:
                    if result == (1, 0):
                        pref =  "train"
                    if result == (0, 1):
                        pref =  "bus"
                    if result == (None, None) or result == (0, 0):
                        pref = input("Specify preference for train or bus").lower()
                else:
                    pref = input("Specify preference for train or bus").lower()

                db_cursor.close()
                close_db_connection(db_connection)

                result = estimated_ticket(fname, person_location, person_destination, funds, pref)
                print(result[0])

                if "Travel itinerary" in result[0]:
                    buy_choice = input("Would you like to buy your ticket?\n").lower()
                    if buy_choice == "yes":
                        purchase_result = purchase_ticket(person_location, person_destination, ticket_price, funds, fname)
                        print(purchase_result)

        elif choice == "info":
            name_tell = input("What is your name?\n").strip()
            get_person_info(name_tell)

        if choice == "schedule":
            pdf_train = "train_schedule.pdf"
            pdf_bus = "bus_schedule.pdf"
            try:
                if os.name == 'nt':  # For Windows
                    if os.path.exists(pdf_train):
                        os.remove("train_schedule.pdf")
                    if os.path.exists(pdf_bus):
                        os.remove("bus_schedule.pdf")
                schedule_pdf()
                if os.name == 'nt':  # For Windows
                    if os.path.exists(pdf_train):
                        os.system(f'start {pdf_train}')
                    if os.path.exists(pdf_bus):
                        os.system(f'start {pdf_bus}')
            except:
                FileNotFoundError
       
        elif choice == "exit":
            print("Exiting program...")
            break
