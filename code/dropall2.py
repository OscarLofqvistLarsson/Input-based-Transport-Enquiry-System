from connection2 import *


db_connection = establish_db_connection()

if db_connection:

    db_cursor = db_connection.cursor()

    db_cursor.execute("SHOW TABLES")

    tables = db_cursor.fetchall()

    for table in tables:
        table_name = table[0]
        drop_query = f"DROP TABLE IF EXISTS {table_name}"
        db_cursor.execute(drop_query)
        print(f"Dropped table: {table_name}")

    db_connection.commit()

    close_db_connection(db_connection)

print("All tables have been dropped")