import mysql.connector as sql

class Conexao:
    def __init__(self):
        self.mydb = sql.connect(
            host="localhost",
            user="root",
            password="",
            database="ifnetwork",
            port=3306
        )
        self.cursor = self.mydb.cursor()
        self.cursor_dict = self.mydb.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.mydb.close()