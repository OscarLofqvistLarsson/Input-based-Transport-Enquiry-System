from datetime import datetime, timedelta

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

            schedule.append((current_time.strftime("%H:%M"), (current_time + travel_time).strftime("%H:%M"),
                             travel_time.total_seconds() // 60, start_station, end_station))

            current_time += travel_time

        # Going back to Sölvesborg
        for i in range(len(locations) - 1, 0, -1):
            start_station = locations[i]
            end_station = locations[i - 1]

            schedule.append((current_time.strftime("%H:%M"), (current_time + travel_time).strftime("%H:%M"),
                             travel_time.total_seconds() // 60, start_station, end_station))

            current_time += travel_time

    return schedule

schedule = populate_schedule()

for entry in schedule:
    print(entry)
