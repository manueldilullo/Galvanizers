import tkinter as tk
from .login_frame import LoginPage
from utils.db import DB_util

class SignupPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller

        self.db = DB_util()
        
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        self.surname_label = tk.Label(self, text="Surname:")
        self.surname_label.grid(row=1, column=0)
        self.surname_entry = tk.Entry(self)
        self.surname_entry.grid(row=1, column=1)

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=2, column=0)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=2, column=1)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=3, column=0)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=1)

        self.age_label = tk.Label(self, text="Age:")
        self.age_label.grid(row=4, column=0)
        self.age_entry = tk.Entry(self)
        self.age_entry.grid(row=4, column=1)

        self.sex_label = tk.Label(self, text="Sex:")
        self.sex_label.grid(row=5, column=0)
        self.sex_male = tk.Checkbutton(self, text="Male")
        self.sex_male.grid(row=5, column=1)
        self.sex_female = tk.Checkbutton(self, text="Female")
        self.sex_female.grid(row=5, column=2)

        self.feeling_label = tk.Label(self, text="How are you feeling?")
        self.feeling_label.grid(row=6, column=0)
        self.feeling_happy = tk.Checkbutton(self, text="Happy😁")
        self.feeling_happy.grid(row=6, column=1)
        self.feeling_sad = tk.Checkbutton(self, text="Sad😔")
        self.feeling_sad.grid(row=6, column=2)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=7, column=1)

    # utility to submit data to DB and switch to LoginPage
    def submit(self):
        # TODO FIX AND IMPLEMENT THIS
        # name = self.name_entry.get()
        # surname = self.surname_entry.get()
        # email = self.email_entry.get()
        # password = self.password_entry.get()
        # age = self.age_entry.get()
        # sex = "Male" if self.sex_male.getvar("value") == 1 else "Female"
        # feeling = "Happy" if self.feeling_happy.getvar("value") == 1 else "Sad"
        # self.db.signup()
        
        self.controller.switch_frame(LoginPage)
        self.controller.title("Login")