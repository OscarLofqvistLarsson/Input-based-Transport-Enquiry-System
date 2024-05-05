from datetime import datetime, timedelta

def populate_schedule():
    locations = ["Sölvesborg", "Karlshamn", "Bräkne-Hoby", "Ronneby", "Bergåsa", "Karlskrona"]
    arrival_time = []
    departure_time = []
    start_station = "Sölvesborg"
    end_station = "Karlskrona"
    start_time = datetime.strptime("06:00", "%H:%M")
    end_time = datetime.strptime("22:00", "%H:%M")
    journey_time = timedelta(minutes=60)
    stop_time = timedelta(minutes=10)

    # Populate schedule from Sölvesborg to Karlskrona
    current_time = start_time
    while current_time < end_time:
        for location in locations:
            arrival_time.append((start_station + "-to " + end_station, location, current_time.strftime("%H:%M")))
            departure_time.append((start_station + "-to " + end_station, location, (current_time + stop_time).strftime("%H:%M")))
            current_time += stop_time

        # Add journey time for the entire route
        current_time += journey_time - stop_time * (len(locations) - 1)

    # Populate schedule from Karlskrona to Sölvesborg
    current_time = start_time
    while current_time < end_time:
        for location in reversed(locations):
            arrival_time.append((end_station + "-to " + start_station, location, current_time.strftime("%H:%M")))
            departure_time.append((end_station + "-to " + start_station, location, (current_time + stop_time).strftime("%H:%M")))
            current_time += stop_time

        # Add journey time for the entire route
        current_time += journey_time - stop_time * (len(locations) - 1)

    return arrival_time, departure_time

arrivals, departures = populate_schedule()

print("Arrivals:")
for arrival in arrivals:
    print(arrival)

print("\nDepartures:")
for departure in departures:
    print(departure)
