from connection import *
from tables import *
from populate_tables import *
from datetime import datetime, timedelta

# från mjukvaru
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


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

        #for row in schedule_data:
         #   print(row)

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
    def get_schedule(transport_type):
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


    db_connection = establish_db_connection()
    if db_connection:
        db_cursor = db_connection.cursor()

        transport_type = 'train' if threshold[0] == 't' else 'bus'
        query_schedule = get_schedule(transport_type)
        db_cursor.execute(query_schedule, (person_location, person_destination, current_datetime))
        query_result = db_cursor.fetchone()


        if query_result:
            depature_time_str, arrival_time, start_station, end_station, total = query_result

            depature_time = datetime.strptime(depature_time_str, "%H:%M:%S")

            current_datetime = current_datetime.strftime('%H:%M:%S')
            depature_time = depature_time.strftime('%H:%M:%S')
            current_datetime = datetime.strptime(current_datetime,'%H:%M:%S')
            depature_time = datetime.strptime(depature_time,'%H:%M:%S')



            wait_time = depature_time - current_datetime
            wait_time = int(wait_time.total_seconds() / 60) # Minuter


            if wait_time > acceptable_wait and transport_type == 'train': # Acceptable_wait är i min
                transport_type = 'bus'
                query_schedule = get_schedule(transport_type)
                db_cursor.execute(query_schedule, (person_location, person_destination, current_datetime))
                query_result = db_cursor.fetchone()

                if query_result:
                    depature_time_str, arrival_time, start_station, end_station, total = query_result
                    print("Departure time (bus):", depature_time_str)

                    depature_time = datetime.strptime(depature_time_str, "%H:%M:%S")
                    wait_time = (depature_time - current_datetime).total_seconds() / 60
                else:
                    return "No available buses or trains match your criteria."
                
            if wait_time > acceptable_wait and transport_type == 'bus': # Acceptable_wait är i min
                transport_type = 'train'
                query_schedule = get_schedule(transport_type)
                db_cursor.execute(query_schedule, (person_location, person_destination, current_datetime))
                query_result = db_cursor.fetchone()

                if query_result:
                    depature_time_str, arrival_time, start_station, end_station, total = query_result
                    print("Departure time (train):", depature_time_str)

                    depature_time = datetime.strptime(depature_time_str, "%H:%M:%S")
                    wait_time = (depature_time - current_datetime).total_seconds() / 60
                else:
                    return "No available buses or trains match your criteria."



            if query_result:
                ticket_price = 100  # ÄNDRA OM DET INTE ÄR BRA NOG ELLER OM DET BARA ÄR SOSSAR SOM ÅKER, DÅ SKA EN BILJETT KOSTA 1000000000000000000000000:-
                if funds >= ticket_price:
                    result = f"Next {transport_type} from {start_station} to {end_station} departs at {depature_time.strftime('%H:%M:%S')}."
                    result += f"\nArrival time: {arrival_time}"
                    result += f"\nTotal travel time: {total}"
                    result += f"\nTicket price: {ticket_price}"
                    return result
                else:
                    return "Insufficient funds for the ticket."
        else:
            return "No available buses or trains match your criteria."

        db_cursor.close()
        close_db_connection(db_connection)
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