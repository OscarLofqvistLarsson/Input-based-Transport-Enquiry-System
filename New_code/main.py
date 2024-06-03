from connection import *
from tables import *
from populate_tables import *


def test(fname):
    db_connection = establish_db_connection()
    if db_connection:
        db_cursor = db_connection.cursor()

        try:
            arg = ('Oscar')
            db_cursor.callproc('GetPreferences', arg)
            

            db_cursor.close()
            close_db_connection(db_connection)


        except mysql.connector.Error as err:
            print(f"Error: {err}")
            db_cursor.close()
            close_db_connection(db_connection)
            return None
    else:
        return None

if __name__ == "__main__":
    name = input("Enter name: ")
    result = test(name)
    if result:
        print(f"Name: {result[0]}, Train Preference: {result[1]}, Bus Preference: {result[2]}")
    else:
        print("No result found or an error occurred.")