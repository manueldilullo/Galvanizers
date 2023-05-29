from pyclbr import Class
import sqlite3
import tkinter.messagebox as messagebox
import tkinter as tk

class DB_util:
    def __init__(self):
        pass

    def signup(self, name, surname, email, password, age, sex, feeling):
        conn = sqlite3.connect('galvadb.db')
            
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

    def login(self, email, password):
        conn = sqlite3.connect('galvadb.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        result = c.fetchall()
        conn.close()

        return result
         
    def get_email(self):
        print("Not implemented yet")
        pass
