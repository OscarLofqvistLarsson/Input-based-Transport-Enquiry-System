from connection import *
from tables import *
from populate_tables import *


def test():
    db_connection = establish_db_connection()
    if db_connection:
        db_cursor = db_connection.cursor()

        arg = ('Oscar',)
        db_cursor.callproc('GetPreferences', arg)

        # Fetch the result from the stored procedure
        for result in db_cursor.stored_results():
            fetched_result = result.fetchone()

        db_cursor.close()
        close_db_connection(db_connection)

        return fetched_result


if __name__ == "__main__":
    result = test()
    if result:
        print(f"Name: {result[0]}, Train Preference: {result[1]}, Bus Preference: {result[2]}")
    else:
        print("No result found or an error occurred.")