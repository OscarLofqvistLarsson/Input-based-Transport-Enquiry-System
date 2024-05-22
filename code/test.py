from connection import *
from tables import *
from populate_tables import *
from datetime import datetime, timedelta

# från mjukvaru
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# List of stations in order
locations = ["Sölvesborg", "Karlshamn", "Bräkne-Hoby", "Ronneby", "Bergåsa", "Karlskrona"]

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

    def get_schedule(transport_type, start_station, end_station, travel_time):
        if transport_type == 'train':
            query_schedule = """
            SELECT CAST(depature_time AS CHAR) AS depature_time, arrival_time, start_station, end_station, total
            FROM train_schedule
            WHERE start_station = %s AND end_station = %s AND depature_time >= %s
            ORDER BY depature_time
            LIMIT 1
            """
        else:
            query_schedule = """
            SELECT CAST(depature_time AS CHAR) AS depature_time, arrival_time, start_station, end_station, total
            FROM bus_schedule
            WHERE start_station = %s AND end_station = %s AND depature_time >= %s
            ORDER BY depature_time
            LIMIT 1
            """
        return query_schedule

    def find_next_station(db_cursor, transport_type, current_station, travel_time, visited_stations):
        query_schedule = """
        SELECT CAST(depature_time AS CHAR) AS depature_time, arrival_time, start_station, end_station, total
        FROM {}_schedule
        WHERE start_station = %s AND depature_time >= %s
        ORDER BY depature_time
        LIMIT 1
        """.format(transport_type)

        db_cursor.execute(query_schedule, (current_station, travel_time))
        for station in db_cursor.fetchall():
            _, _, _, end_station, _ = station
            if end_station not in visited_stations:
                return station
        return None

    db_connection = establish_db_connection()
    if db_connection:
        db_cursor = db_connection.cursor()
        total_travel_time = timedelta()
        current_station = person_location
        travel_map = []
        visited_stations = set()
        transport_type = 'train' if threshold[0] == 't' else 'bus'

        while current_station != person_destination:
            visited_stations.add(current_station)
            find_station = find_next_station(db_cursor, transport_type,current_station, current_datetime, visited_stations)
            if not find_station:
                return "No bus or train match the criteria"

            depature_time_str, arrival_time_delta, start_station, end_station, total = find_station
            print(find_station)
            depature_time = datetime.strptime(depature_time_str, "%H:%M:%S").time()

            depature_datetime = datetime.combine(current_datetime.date(), depature_time)
            arrival_datetime = depature_datetime + arrival_time_delta

            segment_travel_time = arrival_datetime - depature_datetime
            total_travel_time += segment_travel_time
            travel_map.append((depature_time_str, arrival_datetime.time(), start_station, end_station, total))

            current_datetime = arrival_datetime

            # Check if the direction is correct
            current_index = locations.index(current_station)
            next_index = locations.index(end_station)
            final_index = locations.index(person_destination)
            if (next_index > current_index and final_index > current_index) or (next_index < current_index and final_index < current_index):
                current_station = end_station
            else:
                # If the immediate next station is not in the direction, continue to look for other options.
                alternative_station_found = False
                for station in locations[current_index + 1:]:
                    if station not in visited_stations:
                        find_station = find_next_station(db_cursor, transport_type, current_station, current_datetime, visited_stations)
                        if find_station:
                            current_station = end_station
                            alternative_station_found = True
                            break
                if not alternative_station_found:
                    return "No direct route towards the destination found."

        total_minutes = total_travel_time.total_seconds() / 60
        ticket_price = 100
        if funds >= ticket_price:
            result = "Travel itinerary:\n"
            for depature_time_str, arrival_time, start_station, end_station, total in travel_map:
                result += f"From {start_station} to {end_station}, departure at {depature_time_str}, arrival at {arrival_time}\n"
            result += f"Total travel time: {total_minutes} minutes\n"
            result += f"Ticket price: {ticket_price}\n"
            return result
        else:
            return "Insufficient funds for the ticket."
    else:
        return "Connection to database failed"

if __name__ == "__main__":

    choice = input("Would you like to buy a ticket or see the current schedule?\n")
    if choice == "ticket":
        person_location = input("At what station are you at the moment?\n")
        person_destination = input("Where are you planning on heading today?\n")
        threshold = input("Specify preference for train or bus by either entering t1-t10 or b1-b10 respectively\n")
        funds = int(input("How much money do you have for your traveling needs?\n"))

        result = estimated_ticket(person_location, person_destination, threshold, funds) #Estimated ticket ska ställa en fråga om man vill köpa den, inte tillagt
        print(result)
    elif choice == "schedule":

        try:
            os.remove("train_schedule.pdf")
            os.remove("bus_schedule.pdf")
        except:
            FileNotFoundError

        schedule_pdf()