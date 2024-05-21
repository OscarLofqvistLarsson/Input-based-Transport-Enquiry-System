from connection import *
from tables import *
from populate_tables import *

def estimated_ticket(person_location,person_destination,threshold,funds):

    if threshold[0] == "t":
        acceptable_wait = int(threshold[1:]) * 5

    elif threshold[0] == "b":
        acceptable_wait = int(threshold[1:]) * 5

    else:
        return "Input for preference need to start with t or b for train or bus"


    current_datetime = datetime.now().replace(microsecond=0)

    show_depature = current_datetime + timedelta(hours=2)
    selected_depature = show_depature.time().replace(microsecond=0)

    show_max_travel = current_datetime + timedelta(hours=4)
    selected_max = show_max_travel.time().replace(microsecond=0)

    elapsed_time = timedelta()



    db_connection = establish_db_connection()

    if db_connection:

        db_cursor = db_connection.cursor()

        query_schedule = """
        SELECT *
        FROM schedule
        WHERE depature_time = %s AND arrival_time = %s AND total = %s AND start_station = %s AND end_station = %s
        """
        data_query_search = (selected_depature, selected_max, elapsed_time, person_location, person_destination )
        db_cursor.execute(query_schedule, data_query_search)
        query_result = db_cursor.fetchall()

        print(query_result)












if __name__== "__main__":

    person_location = input("At what station are you at the moment?\n")

    person_destination = input("Where are you planing on heading today?\n")

    threshold = input("Specify preference for train or bus by either entering t1-t10 or b1-b10 respectively\n")

    funds = input("How much money do you have for you're traveling needs\n")

    estimated_ticket(person_location, person_destination, threshold, funds)