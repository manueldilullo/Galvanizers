import os
import argparse
import tkinter as tk
from tkinter import *
import sqlite3
import smtplib
import random
import string
from email.mime.text import MIMEText
from numpy import mean
from PIL import Image, ImageTk
from threading import *
import serial
import time
import tkinter.messagebox as messagebox

import csv
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style


CWD = os.path.dirname(os.path.realpath(__file__))
TOPIC = ""
isTest = False

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.titlevar=" "
        self.title("Galvanic Skin Response Tracker")

        self.email = ""
        self.password = ""

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SignupPage, LoginPage, DonePage):
            page_name = F.__name__
            frame = F(master=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        page_name = SlideshowPage.__name__
        donePage_name = DonePage.__name__
        frame = SlideshowPage(master=container, controller=self, donePage=self.frames[donePage_name])
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

        self.sex_var = tk.StringVar()
        self.sex_var.set("Male")  # Set initial value

        self.sex_male = tk.Radiobutton(self, text="Male", variable=self.sex_var, value="Male")
        self.sex_male.grid(row=5, column=1)

        self.sex_female = tk.Radiobutton(self, text="Female", variable=self.sex_var, value="Female")
        self.sex_female.grid(row=5, column=2)

        self.sex_other = tk.Radiobutton(self, text="Other", variable=self.sex_var, value="Other")
        self.sex_other.grid(row=5, column=3)

        self.feeling_label = tk.Label(self, text="How are you feeling?")
        self.feeling_label.grid(row=6, column=0)
        self.feeling_var = tk.StringVar()
        self.feeling_var.set("Happy")  # Set initial value

        self.feeling_happy = tk.Radiobutton(self, text="Happy😁", variable=self.feeling_var, value="Happy")
        self.feeling_happy.grid(row=6, column=1)

        self.feeling_sad = tk.Radiobutton(self, text="Sad😔", variable=self.feeling_var, value="Sad")
        self.feeling_sad.grid(row=6, column=2)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=7, column=1)

    def submit(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        age = self.age_entry.get()
        sex = self.sex_var.get()
        feeling = self.feeling_var.get()

        conn = sqlite3.connect('galvadb.db')
        try:
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

            import re

            def is_password_valid(password):
                # Check minimum length
                if len(password) < 8:
                    return False
                else:
                    return True

            if not is_password_valid(password):
                messagebox.showerror("Error", "Password does not meet the required standards (minimum length).")
                return  # Exit the function if password is invalid

            def is_email_valid(email):
                # Regular expression pattern for email validation
                pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

                # Check if the email matches the pattern
                if re.match(pattern, email):
                    return True
                else:
                    return False

            if not is_email_valid(email):
                messagebox.showerror("Error", "Invalid email address.")
                return  # Exit the function if email is invalid

            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (name, surname, email, password, age, sex, feeling))
            conn.commit()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists.")

        c.close()         
        conn.close()
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
        email = self.email_entry.get()
        password = self.password_entry.get()
        conn = sqlite3.connect('galvadb.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        if len(c.fetchall()) > 0:
             conn.close()
             self.controller.switch_frame(ChooseTopicPage)
        else:
             conn.close()
             self.email_entry.delete(0, tk.END)
             self.password_entry.delete(0, tk.END)
             self.email_entry.config(bg="red")
             self.password_entry.config(bg="red")
        
class ChooseTopicPage(tk.Frame):
    def __init__(self, master, controller, slideShowPage=None):
        
        self.slideShowPage = slideShowPage
        tk.Frame.__init__(self, master)
        self.master = master
        
        self.controller = controller
        
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
        
        if self.slideShowPage is not None:
    
            self.slideShowPage.topic = self.master.topic
        else:
            self.slideShowPage.topic = "topic1"
        

        self.slideShowPage.controller.title("Slideshow " + self.slideShowPage.topic)
        self.slideShowPage.images_folder = os.path.join(CWD, "images", self.master.topic)
        self.slideShowPage.images = list(map(lambda x: os.path.join(self.slideShowPage.images_folder, x), ["image1.jpg", "image2.jpg", "image3.jpg"]))
        self.slideShowPage.image_index = 0
        self.slideShowPage.image_label = tk.Label(self.slideShowPage)
        self.slideShowPage.image_label.grid(row=0, column=0)
        
        self.slideShowPage.start_button.grid(row=0,column=1)


        self.controller.switch_frame(SlideshowPage)
        
class SlideshowPage(tk.Frame):
    def __init__(self, master, controller, donePage=None):
        
        self.donePage = donePage

        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.start_button = tk.Button(self, text="Start", command=self.measure_thread)
        self.start_button.grid(row=0,column=1)

        self.f = Figure(figsize=(5,4), dpi=100,)
        self.a = self.f.add_subplot(111)

        self.a.xaxis.set_visible(False)

        self.canvas = FigureCanvasTkAgg(self.f, self.master)

        #self.ani = animation.FuncAnimation(self.f, self.animate, interval=100)
        self.ani = animation.FuncAnimation(self.f, self.animate, interval=100, save_count=10)


    def animate(self, i):
        self.pullData = open('test_data.csv', 'r').read()
        self.dataArray = self.pullData.split('\n')
        self.xar=[]
        self.yar=[]
        for eachLine in self.dataArray:
            if len(eachLine)>1:
                x,y = eachLine.split(',')
                self.xar.append(float(x))
                self.yar.append(float(y))
        self.a.clear()
        self.a.set_title("gsr over time")
        self.a.plot(self.xar,self.yar)
         


    def measure_thread(self):
        self.start_button.grid_remove()
        
        if not isTest:
            self.ser = serial.Serial('/dev/cu.usbserial-65D2AB33BE')
            self.ser.flushInput()

        self.streamed_data = []
        self.averages = []

        self.stop_threads=False
        self.t1=Thread(target=self.measure)

        self.t1.start()
        self.show_image()

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=1, row=0)


    
    def show_image(self):

        if self.image_index < len(self.images):
            
            self.img = ImageTk.PhotoImage(Image.open(self.images[self.image_index]))
            self.image_label.config(image=self.img)
            self.image_index += 1
            self.image_label.after(6000, self.show_image)
    
        else:
            
            self.stop_threads = True
            self.t1.join()

            self.image_index = 0

            self.averages.append(mean(self.streamed_data[0:60]))
            self.averages.append(mean(self.streamed_data[60:120]))
            self.averages.append(mean(self.streamed_data[120:180]))

            self.donePage.text = "The image you have reacted the most to is the #" + str(self.averages.index(max(self.averages))+1) 
            self.donePage.text += " with average gsr value equal to "
            self.donePage.text += str(max(self.averages))

            self.donePage.max_val.config(text = self.donePage.text)

            self.donePage.img_path = "/image" + str(self.averages.index(max(self.averages))+1)
            self.donePage.img_path += ".jpg"

            self.donePage.img_path = self.images_folder + self.donePage.img_path

            self.donePage.im = Image.open(self.donePage.img_path)
            self.donePage.im.thumbnail((180, 180), Image.Resampling.LANCZOS)

            self.donePage.img = ImageTk.PhotoImage(self.donePage.im)

            self.donePage.image_label.config(image=self.donePage.img)
            

            self.image_label.grid_forget()
            self.done_button = tk.Button(self, text="Done", command=self.done)
            self.done_button.grid(row=1, column=0)

            

    
    def measure(self):

        open("test_data.csv","w")

        self.i = 0

        while True:
            if not isTest:
                ser_read = self.ser.readline()
                ser_read_float = float(ser_read[0:len(ser_read)-2].decode("utf-8"))
                print(ser_read_float)
            else:
                ser_read_float = random.uniform(1,100)
    
            self.streamed_data.append(ser_read_float)

            with open("test_data.csv","a+") as f:
                writer = csv.writer(f,delimiter=",")
                writer.writerow([self.i,ser_read_float])
            
            self.i +=1

            if self.stop_threads:
                break


    def done(self):
        self.canvas.get_tk_widget().grid_remove()
        self.controller.switch_frame(DonePage)
        self.controller.title("Results")
        self.done_button.grid_remove()
        self.start_button.grid(row=0,column=1)
        
class DonePage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        
        self.controller = controller
        
        self.random_number = random.randint(0, 100)
        
        self.max_val = tk.Label(self, text=f"Random Number: {self.random_number}")
        self.max_val.pack(pady=50)

        self.image_label = Label(self)
        self.image_label.pack(pady=45)

        self.email_button = tk.Button(self, text="Send me an email", command=self.send_email)
        self.email_button.pack(pady=10)
        
        self.done_button = tk.Button(self, text="Done", command=self.done)
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

    def done(self):
        self.controller.switch_frame(ChooseTopicPage)
        self.done_button.grid_remove()

        self.controller.title("Choose Topic")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Galvanic Skin Sensor tracker")
    parser.add_argument('--test', '-t', default='n', help='Set it as y or Y if you want to run the program in test environment. Default: n')
    args = parser.parse_args()
    isTest = args.test.lower() == "y"

    app = App()
    app.mainloop()