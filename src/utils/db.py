from pyclbr import Class
import sqlite3
import tkinter.messagebox as messagebox
import tkinter as tk

class DB_util:
    def __init__(self):
        self._public_var = None
        self.db_name = "galvadb.db"

    def signup(self, name, surname, email, password, age, sex, feeling):
        conn = sqlite3.connect(self.db_name)
            
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
                            name TEXT NOT NULL,
                            surname TEXT NOT NULL,
                            email TEXT PRIMARY KEY,
                            password TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            sex TEXT NOT NULL,
                            feeling TEXT NOT NULL
                        )""")

        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (name, surname, email, password, age, sex, feeling))
        conn.commit()
        c.close()         
        conn.close()

    def get_email(self):
        return self._public_var

    def login(self, email, password):        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        result = c.fetchall()
        self._public_var = email
        conn.close()

        return result
        
    def save_data(self, data):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT ,
                        test TEXT,
                        image_index INTEGER,
                        gsr_value REAL, 
                        FOREIGN KEY (email) REFERENCES users(email)
            )''')

        c.execute("INSERT INTO results (email, test, image_index, gsr_value) VALUES (?, ?, ?, ?)", data)
        conn.commit()
        conn.close()
