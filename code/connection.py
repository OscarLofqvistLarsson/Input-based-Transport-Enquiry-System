import mysql.connector

def establish_db_connection():
    """Establish connection to DataBase"""
    try:
        db_connection = mysql.connector.connect(
            host="sql11.freemysqlhosting.net",
            user="sql11701272",
            password="EcRkIJpCM5",
            database="sql11701272"
        )
        return db_connection

    except mysql.connector.Error as e:
        print(f"Error: {str(e)}")

def close_db_connection(db_connection):
    """Close connection to DataBase"""
    if db_connection.is_connected():
        db_connection.close()