from connection import *
from tables import *
from populate_tables import *
from datetime import datetime, timedelta

# från mjukvarukurs (Samuel)
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# List of stations in order
locations_train = ["Sölvesborg", "Karlshamn", "Bräkne-Hoby", "Ronneby", "Bergåsa", "Karlskrona"]
locations_bus = ["Sölvesborg",  "Mörrum", "Karlshamn", "Bräkne-Hoby", "Ronneby","Listerby","Nättraby", "Karlskrona",  "Lyckeby", "Jämjö", ]

def check_time_diff(db_cursor, acceptable_wait, person_location, current_time, person_destination, transport_type_list):
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

    train_wait = (train_departure - current_time).total_seconds() / 60 if train_departure else float('inf')
    bus_wait = (bus_departure - current_time).total_seconds() / 60 if bus_departure else float('inf')

    def is_correct_direction(start, end, destination, locations):
        try:
            start_index = locations.index(start)
            end_index = locations.index(end)
            destination_index = locations.index(destination)
            return (end_index > start_index and destination_index > start_index) or (end_index < start_index and destination_index < start_index)
        except ValueError:
            return False

    if train_wait <= acceptable_wait and is_correct_direction(person_location, train_end_station, person_destination, locations_train):
        return 'train', train_departure
    elif bus_wait <= acceptable_wait and is_correct_direction(person_location, bus_end_station, person_destination, locations_bus):
        return 'bus', bus_departure
    else:
        if train_wait < bus_wait and is_correct_direction(person_location, train_end_station, person_destination, locations_train):
            return 'train', train_departure
        elif bus_wait < train_wait and is_correct_direction(person_location, bus_end_station, person_destination, locations_bus):
            return 'bus', bus_departure
        else:
            return 'bus', bus_departure if bus_wait < float('inf') else ('train', train_departure if train_wait < float('inf') else None)

def schedule_pdf():
    transport_type = input("Would you like to see the train or bus schedule?\n").strip().lower()
    db_connection = establish_db_connection()

    if db_connection:
        db_cursor = db_connection.cursor()

        if transport_type == "train":
            query_schedule = "SELECT * FROM train_schedule"
            schedule_title = "Train Schedule"
        elif transport_type == "bus":
            query_schedule = "SELECT * FROM bus_schedule"
            schedule_title = "Bus Schedule"
        else:
            print("Invalid choice.")
            exit()

        db_cursor.execute(query_schedule)
        schedule_data = db_cursor.fetchall()
        db_cursor.close()
        close_db_connection(db_connection)

        if not schedule_data:
            print("No schedule data available.")
            exit()

        pdf_filename = f"{transport_type}_schedule.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica", 14)
        c.drawString(30, height - 40, schedule_title)
        c.setFont("Helvetica", 12)

        line_height = 20
        y = height - 60
        for row in schedule_data:
            row_str = " | ".join(str(item) for item in row)
            c.drawString(30, y, row_str)
            y -= line_height
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 40

        c.save()

        print(f"{schedule_title} has been saved as {pdf_filename}.")
    else:
        print("Connection to database failed.")

def estimated_ticket(person_location, person_destination, threshold, funds):
    if threshold[0] == "t" or threshold[0] == "b":
        acceptable_wait = int(threshold[1:]) * 5
    else:
        return "Input for preference needs to start with t or b for train or bus"

    current_datetime = datetime.now().replace(microsecond=0)
    global ticket_price
    ticket_price = 0 

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

    # Kolla så att man inte har stavat fel eller något liknande
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
                                      # Här används inte next_departure, skla det vara såå??????
        transport_type, next_departure = check_time_diff(db_cursor, acceptable_wait, person_location, current_datetime, person_destination, locations_train if threshold[0] == 't' else locations_bus)
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
                locations = locations_train                                     # Används inte location???????????????
            else:
                current_index = locations_bus.index(current_station)
                next_index = locations_bus.index(end_station)
                final_index = locations_bus.index(person_destination)
                locations = locations_bus                                       # Används inte location??????????????? Samma är???????

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
            ticket_price += 50                                             # Här används inte next_departure, skla det vara såå??????
            transport_type, next_departure = check_time_diff(db_cursor, acceptable_wait, current_station, current_datetime, person_destination, locations_train if transport_type == 'train' else locations_bus)
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



def purchase_ticket(location, destination, ticket_price, threshold, funds):
    db_connection = establish_db_connection()
    if db_connection:
        db_cursor = db_connection.cursor()

        new_funds = funds - ticket_price

        insert_ticket_query = """
        INSERT INTO ticket (location, destination, price)
        VALUES (%s, %s, %s)
        """
        db_cursor.execute(insert_ticket_query, (location, destination, ticket_price))
        ticket_id = db_cursor.lastrowid # Får id från förra auto increment

        insert_people_query = """
        INSERT INTO people (threshold, funds,  people_ticketID)
        VALUES (%s, %s, %s)
        """
        db_cursor.execute(insert_people_query, (threshold, new_funds, ticket_id))

        db_connection.commit()
        close_db_connection(db_connection)

        print(f"Ticket purchased for from {location} to {location}.")
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

        if "Travel itinerary" in result:
            buy_choice = input("Would you like to buy you ticket? ")
            if buy_choice.lower() == "yes":
                purchase_ticket(person_location, person_destination, ticket_price, threshold, funds)

    elif choice == "schedule":
        try:
            os.remove("train_schedule.pdf")
            os.remove("bus_schedule.pdf")
        except:
            FileNotFoundError

        schedule_pdf()
