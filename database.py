import mysql.connector
from mysql.connector import Error
import os

DB_HOST = os.environ["DATABASE_HOST"]
DB_PORT = os.environ["DATABASE_PORT"]
DB_USER = os.environ["DATABASE_USERNAME"]
DB_PASSWORD = os.environ["DATABASE_PASSWORD"]
DB_NAME = os.environ["DATABASE_NAME"]

class Database:

    def __init__(self):
        try:
            # Establish the connection to MySQL without specifying the database
            self.con = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                charset="utf8mb4",
                collation="utf8mb4_general_ci"
            )

            if self.con.is_connected():
                print("Successfully connected to the MySQL server")

            self.cur = self.con.cursor()

            # Check if the database exists, and if not, create it
            self.cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
            self.con.commit()  # Commit the changes

            # Now connect to the specific database
            self.con.database = DB_NAME

            # Create the 'chats' table if it does not exist
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS chats (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    chatID BIGINT,
                    latitude FLOAT,
                    longitude FLOAT
                )
            ''')

            # Commit the changes
            self.con.commit()

        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            self.con = None
            self.cur = None

    def __del__(self):
        if self.con and self.con.is_connected():
            self.cur.close()
            self.con.close()
            print("MySQL connection closed")

    def get_chats(self):
        ''' Return a list of all chats '''
        try:
            query = "SELECT * FROM chats"
            self.cur.execute(query)
            return self.cur.fetchall()
        except Error as e:
            print(f"Error fetching chats: {e}")
            return []

    def get_chat(self, id):
        ''' Return a specific chat by chatID '''
        try:
            query = "SELECT * FROM chats WHERE chatID = %s"
            self.cur.execute(query, (id,))
            return self.cur.fetchone()
        except Error as e:
            print(f"Error fetching chat: {e}")
            return None

    def set_latitude(self, latitude, id):
        ''' Update latitude for a chat '''
        try:
            query = "UPDATE chats SET latitude = %s WHERE chatID = %s"
            self.cur.execute(query, (latitude, id))
            self.con.commit()
        except Error as e:
            print(f"Error updating latitude: {e}")

    def set_longitude(self, longitude, id):
        ''' Update longitude for a chat '''
        try:
            query = "UPDATE chats SET longitude = %s WHERE chatID = %s"
            self.cur.execute(query, (longitude, id))
            self.con.commit()
        except Error as e:
            print(f"Error updating longitude: {e}")

    def create_chat(self, id):
        ''' Create a chat with a given chatID '''
        try:
            query = "INSERT INTO chats (chatID, latitude, longitude) VALUES (%s, %s, %s)"
            self.cur.execute(query, (id, 0, 0))
            self.con.commit()
        except Error as e:
            print(f"Error creating chat: {e}")
