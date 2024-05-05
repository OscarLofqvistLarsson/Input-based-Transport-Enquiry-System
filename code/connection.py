import mysql.connector

def establish_db_connection():
    """Establish connection to DataBase"""
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="user",
            password="EcRkIJpCM5",
            database="project_DV1663"
        )
        return db_connection

    except mysql.connector.Error as e:
        print(f"Error: {str(e)}")

def close_db_connection(db_connection):
    """Close connection to DataBase"""
    if db_connection.is_connected():
        db_connection.close()