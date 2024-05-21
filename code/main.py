import datetime
from connection import *
from dropall import *
from tables import *
from populate_tables import *

def estimated_ticket(person_location,person_destination,threshold,funds):

    if threshold[0] == "t":
        acceptable_wait = int(threshold[1:]) * 5

    elif threshold[0] == "b":
        acceptable_wait = int(threshold[1:]) * 5

    else:
        return "Input for preference need to start with t or b for train or bus"


    current_time = datetime.datetime.now().time().replace(microsecond=0)

    print(current_time)

    db_connection = establish_db_connection()

    if db_connection:

        db_cursor = db_connection.cursor()
        
        query = ("SELECT start_station WHERE (start_station = %s) AND (departure_time = %s)"(person_location, person_location,))
        db_cursor.execute(query)












if __name__== "__main__":

    person_location = input("At what station are you at the moment?\n")

    person_destination = input("Where are you planing on heading today?\n")

    threshold = input("Specify preference for train or bus by either entering t1-t10 or b1-b10 respectively\n")

    funds = input("How much money do you have for you're traveling needs\n")

    estimated_ticket(person_location, person_destination, threshold, funds)