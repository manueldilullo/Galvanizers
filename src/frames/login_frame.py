import tkinter as tk
from .topic_frame import ChooseTopicPage
from utils.db import DB_util
import tkinter.messagebox as messagebox


class LoginPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller

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

        fields = {
            "Email": self.email_entry,
            "Password": self.password_entry
        }

        values = {}
        for field, widget in fields.items():
            values[field] = widget.get()

        email = values["Email"]
        password = values["Password"]
       
       #check length of entry
        for field, entry in fields.items():
            value = entry.get()
            if len(value) == 0:
                messagebox.showerror("Error", f"{field} is required.")
                return
            
        result = self.controller.db_util.login(email, password)

        if len(result) <= 0:
            messagebox.showerror("Error", "Invalid Credentials.")
            return
        else:
            self.controller.switch_frame(ChooseTopicPage)
            self.controller.title("Choose Topic")
