from connection import *
from tables import *
from populate_tables import *
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def schedule_pdf():
    transport_type = input("Would you like to see the train or bus schedule?\n").strip().lower()
    db_connection = establish_db_connection()

    if db_connection:
        db_cursor = db_connection.cursor()

        if transport_type == "train":
            query_schedule = """
            SELECT ts.departure_time, ts.arrival_time, ts.start_station, t1.ID AS start_station_id, ts.end_station, t2.ID AS end_station_id, ts.total
            FROM train_schedule ts
            JOIN train t1 ON ts.start_station = t1.location
            JOIN train t2 ON ts.end_station = t2.location
            """
            schedule_title = "Train Schedule"

        elif transport_type == "bus":
            query_schedule = """
            SELECT bs.departure_time, bs.arrival_time, bs.start_station, b1.ID AS start_station_id, bs.end_station, b2.ID AS end_station_id, bs.total
            FROM bus_schedule bs
            JOIN bus b1 ON bs.start_station = b1.location
            JOIN bus b2 ON bs.end_station = b2.location
            """
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