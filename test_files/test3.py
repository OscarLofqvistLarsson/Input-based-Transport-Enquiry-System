import mysql.connector
from datetime import datetime, timedelta

# Function to generate the train schedule
def populate_schedule():
    locations = ["Sölvesborg", "Karlshamn", "Bräkne-Hoby", "Ronneby", "Bergåsa", "Karlskrona"]
    start_time = datetime.strptime("06:00", "%H:%M")
    end_time = datetime.strptime("22:00", "%H:%M")
    delta_time = timedelta(minutes=10)
    travel_time = timedelta(minutes=10)  # Assuming each leg of the journey takes 10 minutes

    schedule = []

    current_time = start_time
    while current_time < end_time:
        # Going from Sölvesborg to Karlskrona
        for i in range(len(locations) - 1):
            start_station = locations[i]
            end_station = locations[i + 1]

            schedule.append((current_time.strftime("%Y-%m-%d %H:%M:%S"), (current_time + travel_time).strftime("%Y-%m-%d %H:%M:%S"),
                            str(travel_time), start_station, end_station))

            current_time += travel_time

        # Going back to Sölvesborg
        for i in range(len(locations) - 1, 0, -1):
            start_station = locations[i]
            end_station = locations[i - 1]

            schedule.append((current_time.strftime("%Y-%m-%d %H:%M:%S"), (current_time + travel_time).strftime("%Y-%m-%d %H:%M:%S"),
                            str(travel_time), start_station, end_station))

            current_time += travel_time

    # Adding another train starting from Karlskrona and going in the opposite direction
    current_time = start_time
    while current_time < end_time:
        # Going from Karlskrona to Sölvesborg
        for i in range(len(locations) - 1, 0, -1):
            start_station = locations[i]
            end_station = locations[i - 1]

            schedule.append((current_time.strftime("%Y-%m-%d %H:%M:%S"), (current_time + travel_time).strftime("%Y-%m-%d %H:%M:%S"),
                            str(travel_time), start_station, end_station))

            current_time += travel_time

        # Going back to Karlskrona
        for i in range(len(locations) - 1):
            start_station = locations[i]
            end_station = locations[i + 1]

            schedule.append((current_time.strftime("%Y-%m-%d %H:%M:%S"), (current_time + travel_time).strftime("%Y-%m-%d %H:%M:%S"),
                            str(travel_time), start_station, end_station))

            current_time += travel_time

    return schedule

# Function to populate the schedule into the MySQL database
def populate_mysql_schedule(schedule):
    conn = mysql.connector.connect(
        host="localhost",
        user="user",
        password="EcRkIJpCM5",
        database="project_DV1663"
    )
    cursor = conn.cursor()

    create_schedule_table = """
        CREATE TABLE IF NOT EXISTS schedule(
            depature_time DATETIME NOT NULL,
            arrival_time DATETIME NOT NULL,
            total VARCHAR(255) NOT NULL,
            start_station VARCHAR(255) NOT NULL,
            end_station VARCHAR(255) NOT NULL
        )
    """

    cursor.execute(create_schedule_table)

    insert_query = "INSERT INTO schedule (depature_time, arrival_time, total, start_station, end_station) VALUES (%s, %s, %s, %s, %s)"

    for entry in schedule:
        depature_time, arrival_time, total, start_station, end_station = entry
        values = (depature_time, arrival_time, total, start_station, end_station)
        cursor.execute(insert_query, values)

    conn.commit()

    cursor.close()
    conn.close()

# Generate the train schedule
schedule = populate_schedule()

# Populate the schedule into the MySQL database
populate_mysql_schedule(schedule)
