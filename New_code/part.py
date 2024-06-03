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

def add_people():
    db_connection = establish_db_connection()
    if db_connection:
        try:
            db_cursor = db_connection.cursor()
            new_name = input("What is your name?\n")
            new_funds = input("How much money do you have?\n")

            INSERT_PEOPLE = """
                INSERT INTO people (fname, funds)
                VALUES (%s, %s)
            """
            db_cursor.execute(INSERT_PEOPLE, (new_name, new_funds,))
            db_connection.commit()


        except mysql.connector.Error as err:
            print(f"Error: {err}")
            db_connection.rollback()
        finally:
            db_cursor.close()
            close_db_connection(db_connection)
    else:
        print("Connection to database failed")

if __name__ == "__main__":
    choice = input("To add a profile, type 'profile'.\n")
    if choice == 'profile':
        add_people()
    result = test()
    if result:
        print(f"Name: {result[0]}, Train Preference: {result[1]}, Bus Preference: {result[2]}")
    else:
        print("No result found or an error occurred.")