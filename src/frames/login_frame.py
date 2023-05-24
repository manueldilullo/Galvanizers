import tkinter as tk
from .topic_frame import ChooseTopicPage

from utils.db import DB_util

class LoginPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        
        self.db = DB_util()

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 4), weight=1)

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=1, column=0, sticky="e")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1, sticky="w")

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=2, column=0, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, sticky="w")

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2)

    def login(self):
        # TODO IMPLEMENT AND FIX THIS
        # self.db.login()
        self.controller.switch_frame(ChooseTopicPage)
        self.controller.title("Choose Topic")
