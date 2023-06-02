import sqlite3
from datetime import datetime

import tkinter as tk
import tkinter.messagebox as messagebox
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

        c.execute("""SELECT email
                   FROM users
                   WHERE email=?
                       """,
                (email,))
        result = c.fetchone()

        if result:
            # Record already exists
            messagebox.showerror("Error","Email already registered")

        else:
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
    
    def create_result_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT ,
                        test TEXT,
                        topic TEXT,
                        image_index INTEGER,
                        gsr_value REAL, 
                        timestamp TEXT,
                        FOREIGN KEY (email) REFERENCES users(email)
            )''')
        conn.commit()
        conn.close()
        
    def save_data(self, data):
        self.create_result_table()
        
        # Get the current UTC time
        current_time = datetime.now()

        # Format the time as a string in GMT format
        time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print(time_str)
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute("INSERT INTO results (email, test, topic, image_index, gsr_value, timestamp) VALUES (?, ?, ?, ?, ?, ?)", data + (time_str, ))
        conn.commit()
        conn.close()
        
    def get_user_data(self, email):
        self.create_result_table()
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        conn.row_factory = lambda cursor, row: row[0]
        results = c.execute("SELECT id, email, test, topic, image_index, gsr_value, timestamp FROM results WHERE email=?", (email,)).fetchall()
        conn.commit()
        conn.close()
        
        return results
    