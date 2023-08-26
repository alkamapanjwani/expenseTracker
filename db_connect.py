import psycopg2
from config import DB_HOST,DB_NAME,DB_USER,DB_PASS
class DB:
    def __init__(self):
        self.conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        self.cursor = self.conn.cursor()

    def execute_fetchone(self, query, query_params):
        self.cursor.execute(query, query_params)
        return self.cursor.fetchone()


    def destroy(self):
        self.cursor.close()
        self.conn.close()
