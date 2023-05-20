import tkinter as tk
from .topic_frame import ChooseTopicPage

from utils.db import DB_util

class LoginPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        
        self.db = DB_util()

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=0, column=0)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2, column=1)

    def login(self):
        # TODO IMPLEMENT AND FIX THIS
        # self.db.login()
        self.controller.switch_frame(ChooseTopicPage)
        self.controller.title("Choose Topic")
