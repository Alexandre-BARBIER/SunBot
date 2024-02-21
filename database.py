from sqlite3 import connect


DATABASE_NAME = "Sun.db"

'''Définir la base de donnée'''
class Database:

    def __init__(self):

        self.con = connect(DATABASE_NAME)
        self.cur = self.con.cursor()

        # id is the Telegram individual id
        self.cur.execute('''CREATE TABLE IF NOT EXISTS chats(
            id INTEGER PRIMARY KEY,
            chatID INTEGER,
            latitude FLOAT,
            longitude FLOAT
        )''')

        self.con.commit()

    def get_chats(self):
        ''' Return a list of all verified people '''

        query = "SELECT * FROM chats"
        queryValues = ()
        res = self.cur.execute(query, queryValues).fetchall()
        return res

    def get_chat(self, id):
        ''' Return a list of all verified people '''

        query = "SELECT * FROM chats WHERE chatID = (?)"
        queryValues = (id,)
        res = self.cur.execute(query, queryValues).fetchone()
        return res

    def setLatitude(self, latitude, id):
        ''' Add latitude for a chat '''
        query = "UPDATE chats SET latitude = (?) WHERE chatID = (?)"
        queryValues = (latitude, id)
        self.cur.execute(query, queryValues)
        self.con.commit()

    def setLongitude(self, longitude, id):
        ''' Add longitude for a chat '''
        query = "UPDATE chats SET longitude = (?) WHERE chatID = (?)"
        queryValues = (longitude, id)
        self.cur.execute(query, queryValues)
        self.con.commit()

    def createChat(self, id):
        ''' Create a chat with id '''

        query = "INSERT INTO chats (chatID, latitude, longitude) VALUES (?, ?, ?)"
        queryValues = (id, 0, 0)
        self.cur.execute(query, queryValues)
        self.con.commit()
