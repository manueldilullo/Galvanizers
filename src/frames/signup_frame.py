from email import utils
import tkinter as tk
from .login_frame import LoginPage
import tkinter.messagebox as messagebox
import re
from utils.db import DB_util


class SignupPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        
        self.master = master
        self.controller = controller
        
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 9), weight=1)

        # Name
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.grid(row=1, column=0, sticky="e")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=1, column=1, sticky="w")

        # Surname
        self.surname_label = tk.Label(self, text="Surname:")
        self.surname_label.grid(row=2, column=0, sticky="e")
        self.surname_entry = tk.Entry(self)
        self.surname_entry.grid(row=2, column=1, sticky="w")

        # Email
        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=3, column=0, sticky="e")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=3, column=1, sticky="w")

        # Password
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=4, column=0, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=4, column=1, sticky="w")

        # Age
        self.age_label = tk.Label(self, text="Age:")
        self.age_label.grid(row=5, column=0, sticky="e")
        self.age_entry = tk.Entry(self)
        self.age_entry.grid(row=5, column=1, sticky="w")

        # Sex
        self.sex_label = tk.Label(self, text="Gender:")
        self.sex_label.grid(row=6, column=0, sticky="e")

        self.sex_var = tk.StringVar()
        self.sex_var.set("Male")  # Set initial value

        self.sex_frame = tk.Frame(self)
        self.sex_frame.grid(row=6, column=1, sticky="w")

        self.sex_male = tk.Radiobutton(self.sex_frame, text="Male", variable=self.sex_var, value="Male")
        self.sex_male.grid(row=0, column=0, sticky="w")
        self.sex_female = tk.Radiobutton(self.sex_frame, text="Female", variable=self.sex_var, value="Female")
        self.sex_female.grid(row=0, column=1, sticky="w")
        self.sex_other = tk.Radiobutton(self.sex_frame, text="Other", variable=self.sex_var, value="Other")
        self.sex_other.grid(row=0, column=2, sticky="w")

        # Feeling
        self.feeling_label = tk.Label(self, text="How are you feeling?")
        self.feeling_label.grid(row=7, column=0, sticky="e")

        self.feeling_var = tk.StringVar()
        self.feeling_var.set("Neutral")  # Set initial value

        self.feeling_frame = tk.Frame(self)
        self.feeling_frame.grid(row=7, column=1, sticky="w")

        self.feeling_anxious = tk.Radiobutton(self.feeling_frame, text="Anxious", variable=self.feeling_var, value="Anxious")
        self.feeling_anxious.grid(row=0, column=0, sticky="w")
        self.feeling_neutral = tk.Radiobutton(self.feeling_frame, text="Neutral", variable=self.feeling_var, value="Neutral")
        self.feeling_neutral.grid(row=0, column=1, sticky="w")
        self.feeling_happy = tk.Radiobutton(self.feeling_frame, text="Happy", variable=self.feeling_var, value="Happy")
        self.feeling_happy.grid(row=0, column=2, sticky="w")
        
        # Submit
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=8, column=0, columnspan=2)
        self.login_button = tk.Button(self, text="Already signed up?", command=self.go_to_login)
        self.login_button.grid(row=9, column=0, columnspan=2)

    # utility to submit data to DB and switch to LoginPage
    def submit(self):
        fields = {
            "Name": self.name_entry,
            "Surname": self.surname_entry,
            "Email": self.email_entry,
            "Password": self.password_entry,
            "Age": self.age_entry,
            "Sex": self.sex_var,
            "Feeling": self.feeling_var
        }

        values = {}
        for field, widget in fields.items():
            values[field] = widget.get()

        name = values["Name"]
        surname = values["Surname"]
        email = values["Email"]
        password = values["Password"]
        age = values["Age"]
        sex = values["Sex"]
        feeling = values["Feeling"]

        #check length of entry
        for field, entry in fields.items():
            value = entry.get()
            if len(value) == 0:
                messagebox.showerror("Error", f"{field} is required.")
                return
        
        #check minimum length of password
        def is_password_valid(password):
            return len(password) > 8

        if not is_password_valid(password):
            messagebox.showerror("Error", "Password does not meet the required standards (minimum length is 8).")
            return # Exit the function if password is invalid

        #check email pattern
        def is_email_valid(email):
                pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

                if re.match(pattern, email):
                    return True
                else:
                    return False

        if not is_email_valid(email):
            messagebox.showerror("Error", "Invalid email address.")
            return 

        #check if age is in normal range
        def is_valid_age(age):
                age = int(age)
                return (age >= 1 and age <= 120)
                
        if not is_valid_age(age):
            messagebox.showerror("Error", "Invalid age. Please enter a value between 1 and 120.")
            return     
        
        db_util = DB_util()
        db_util.signup(name,surname,email,password,age,sex,feeling)
        
        self.controller.switch_frame(LoginPage)
        self.controller.title("Login")
    
    # Change frame to login frame
    def go_to_login(self):
        self.controller.switch_frame(LoginPage)
        self.controller.title("Login")