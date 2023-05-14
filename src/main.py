import os
import tkinter as tk
from tkinter import *
import sqlite3
import smtplib
import random
import string
from email.mime.text import MIMEText
from PIL import Image, ImageTk

CWD = os.path.dirname(os.path.realpath(__file__))

WINDOW_SIZES = [500, 500]
RESIZABLE_SIZES = (0, 0)
IMAGES_SIZES = (250, 250)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.titlevar=" "
        self.title("Galvanic Skin Response Tracker")

        self.email = ""
        self.password = ""

        self.geometry(f"{WINDOW_SIZES[0]}x{WINDOW_SIZES[1]}")
        self.resizable = RESIZABLE_SIZES
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SignupPage, LoginPage, SlideshowPage, DonePage):
            page_name = F.__name__
            frame = F(master=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        page_name = ChooseTopicPage.__name__
        slideShowpage_name = SlideshowPage.__name__
        frame = ChooseTopicPage(master=container, controller=self, slideShowPage=self.frames[slideShowpage_name])
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.switch_frame(SignupPage)
        self.title("Signup")

    def switch_frame(self, page_class):
        frame = self.frames[page_class.__name__]
        frame.tkraise()
        
class SignupPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        
        self.controller = controller

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

    def submit(self):
        # TODO FIX THIS
        # name = self.name_entry.get()
        # surname = self.surname_entry.get()
        # email = self.email_entry.get()
        # password = self.password_entry.get()
        # age = self.age_entry.get()
        # sex = "Male" if self.sex_male.getvar("value") == 1 else "Female"
        # feeling = "Happy" if self.feeling_happy.getvar("value") == 1 else "Sad"
        
        # conn = sqlite3.connect('user.db')
        # c = conn.cursor()
        # c.execute('''CREATE TABLE IF NOT EXISTS users
        #              (name text, surname text, email text, password text, age integer, sex text, feeling text)''')
        # c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (name, surname, email, password, age, sex, feeling))
        # conn.commit()
        # conn.close()
        self.controller.switch_frame(LoginPage)
        self.controller.title("Login")

class LoginPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master

        self.controller = controller

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
        self.controller.switch_frame(ChooseTopicPage)
        self.controller.title("Choose Topic")
        # email = self.email_entry.get()
        # password = self.password_entry.get()
        # conn = sqlite3.connect('user.db')
        # c = conn.cursor()
        # c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        # if len(c.fetchall()) > 0:
        #     conn.close()
        #     self.controller.switch_frame(ChooseTopicPage)
        # else:
        #     conn.close()
        #     self.email_entry.delete(0, tk.END)
        #     self.password_entry.delete(0, tk.END)
        #     self.email_entry.config(bg="red")
        #     self.password_entry.config(bg="red")
        
class ChooseTopicPage(tk.Frame):
    def __init__(self, master, controller, slideShowPage=None):
        tk.Frame.__init__(self, master)
        
        self.master = master
        self.controller = controller
        self.slideShowPage = slideShowPage
        
        self.topic_label = tk.Label(self, text="Choose a topic:")
        self.topic_label.grid(row=0, column=0)

        self.topics = ["Topic1", "Topic2", "Topic3"]
        self.topic_var = tk.StringVar()
        self.topic_var.set(self.topics[0])
        self.topic_dropdown = tk.OptionMenu(self, self.topic_var, *self.topics)
        self.topic_dropdown.grid(row=0, column=1)

        self.done_button = tk.Button(self, text="Done", command=self.done)
        self.done_button.grid(row=1, column=1)

    def done(self):
        self.master.topic = self.topic_var.get()
        self.slideShowPage.topic = self.master.topic
        self.slideShowPage.controller.title("Slideshow " + self.slideShowPage.topic)

        self.slideShowPage.images_folder = os.path.join(CWD, "images", self.master.topic)
        self.slideShowPage.images = list(map(lambda x: os.path.join(self.slideShowPage.images_folder, x), ["image1.jpg", "image2.jpg", "image3.jpg"]))
        self.slideShowPage.image_index = 0
        self.slideShowPage.image_label = tk.Label(self.slideShowPage)
        self.slideShowPage.image_label.place(relx=.5, rely=.35, anchor="c")

        self.slideShowPage.show_image()

        self.controller.switch_frame(SlideshowPage)
        
class SlideshowPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller

    def show_image(self):
        if self.image_index < len(self.images):
            print(self.images[self.image_index])
            
            image_bin = Image.open(self.images[self.image_index])
            image_bin = image_bin.resize(IMAGES_SIZES, Image.ANTIALIAS)
            
            self.img = ImageTk.PhotoImage(image_bin)
            
            self.image_label.config(image=self.img)
            self.image_index += 1
            self.image_label.after(6000, self.show_image)
        else:
            self.done_button = tk.Button(self, text="Done", command=self.done)
            self.done_button.place(relx=.5, rely=.65, anchor="c")

    def done(self):
        self.controller.switch_frame(DonePage)
        self.controller.title("Random Number")
        
class DonePage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        
        self.controller = controller
        
        self.random_number = random.randint(0, 100)
        
        self.random_label = tk.Label(self, text=f"Random Number: {self.random_number}")
        self.random_label.pack(pady=50)

        self.email_button = tk.Button(self, text="Send me an email", command=self.send_email)
        self.email_button.pack(pady=10)
        
        self.done_button = tk.Button(self, text="Done", font=("Helvetica", 14), command=lambda: controller.switch_frame(ChooseTopicPage))
        self.done_button.pack(pady=10)
        
    def send_email(self):
        # TODO IMPLEMENT THIS
        # email = self.master.email
        # password = self.master.password
        # message = f"Subject: Random Number\n\n{self.random_number}"
        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        #     server.login(email, password)
        #     server.sendmail(email, email, message)
        # messagebox.showinfo("Email sent", "The email has been sent to your address.")
        self.controller.switch_frame(ChooseTopicPage)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
