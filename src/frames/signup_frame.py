import tkinter as tk
from .login_frame import LoginPage
from utils.db import DB_util

class SignupPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        
        self.master = master
        self.controller = controller

        self.db = DB_util() 
        
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 9), weight=1)

        self.name_label = tk.Label(self, text="Name:")
        self.name_label.grid(row=1, column=0, sticky="e")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=1, column=1, sticky="w")

        self.surname_label = tk.Label(self, text="Surname:")
        self.surname_label.grid(row=2, column=0, sticky="e")
        self.surname_entry = tk.Entry(self)
        self.surname_entry.grid(row=2, column=1, sticky="w")

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=3, column=0, sticky="e")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=3, column=1, sticky="w")

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=4, column=0, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=4, column=1, sticky="w")

        self.age_label = tk.Label(self, text="Age:")
        self.age_label.grid(row=5, column=0, sticky="e")
        self.age_entry = tk.Entry(self)
        self.age_entry.grid(row=5, column=1, sticky="w")

        self.sex_label = tk.Label(self, text="Gender:")
        self.sex_label.grid(row=6, column=0, sticky="e")

        self.sex_frame = tk.Frame(self)
        self.sex_frame.grid(row=6, column=1, sticky="w")

        self.sex_male = tk.Checkbutton(self.sex_frame, text="Male")
        self.sex_male.grid(row=0, column=1, sticky = "ew")
        self.sex_female = tk.Checkbutton(self.sex_frame, text="Female")
        self.sex_female.grid(row=0, column=2, sticky = "ew")

        self.feeling_label = tk.Label(self, text="How are you feeling?")
        self.feeling_label.grid(row=7, column=0, sticky="e")

        self.feeling_frame = tk.Frame(self)
        self.feeling_frame.grid(row=7, column=1, sticky="w")

        self.feeling_happy = tk.Checkbutton(self.feeling_frame, text="Happy😁")
        self.feeling_happy.grid(row=0, column=1, sticky="ew")
        self.feeling_sad = tk.Checkbutton(self.feeling_frame, text="Sad😔")
        self.feeling_sad.grid(row=0, column=2, sticky="ew")

        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=8, column=0, columnspan=2)

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