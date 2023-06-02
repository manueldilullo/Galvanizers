import os
import tkinter as tk

import time
import random
import serial
from threading import Thread

import csv
import json

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

from PIL import Image, ImageTk

from .done_frame import DonePage

class SlideshowPage(tk.Frame):
    def __init__(self, master, controller, donePage=None, isTest=False):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.donePage = donePage
        
        self.isTest = isTest
        self.time_per_image = int(self.controller.config["slideshow"]["pic_show_time"])
        self.image_sizes = tuple(self.controller.config["sizes"]["image_sizes"])
        
        self.msg = tk.Label(self, text="You will be shown a sequence of images. Please focus on it. \n Remember to wear the sensors on your fingers. \n When ready, press start. \n")

        self.start_button = tk.Button(self, text="Start", command=self.measure_thread)
        self.start_button.place(relx=0.5, rely=0.60, anchor=tk.CENTER)

        # set up plot
        self.f = Figure(figsize=(4,4), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.xaxis.set_visible(False)
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.ani = animation.FuncAnimation(self.f, self.animate, interval=100)

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
        self.start_button.place_forget()
        self.msg.place_forget()
        
        if not self.isTest:
            self.ser = serial.Serial('/dev/cu.usbserial-65D2AB33BE')
            self.ser.flushInput()

        self.streamed_data = []

        self.stop_threads=False
        self.t1=Thread(target=self.measure)

        self.t1.start()
        self.show_image()

        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.60, rely=0.5, anchor=tk.W)
    
    def show_image(self):
        if self.image_index < len(self.images):
            print(self.images[self.image_index])
            
            image_bin = Image.open(self.images[self.image_index])
            image_bin = image_bin.resize(self.image_sizes, Image.ANTIALIAS)
            
            self.img = ImageTk.PhotoImage(image_bin)
            self.image_label.config(image=self.img)
            self.image_label.place(relx=0.1, rely=0.5, anchor=tk.W)
            self.image_index += 1
            self.image_label.after(self.time_per_image, self.show_image)
    
        else:
            self.stop_threads = True
            self.t1.join()
            self.image_index = 0

            self.font = tk.font.Font(size=24)
            self.done_button = tk.Button(self, text="Done", command=self.done)
            self.done_button["font"] = self.font
            self.done_button.place(relx=.5, rely=.85, anchor=tk.S)
    
    def measure(self):
        
        self.i = 0
        while True:
            if not self.isTest:
                ser_read = self.ser.readline()
                ser_read_float = float(ser_read[0:len(ser_read)-2].decode("utf-8"))
                print(ser_read_float)
            else:
                ser_read_float = random.uniform(1,100)
    
            self.streamed_data.append(ser_read_float)

            with open("test_data.csv","a+") as self.f:
                if self.i==0 :
                    self.f.truncate(0)
                writer = csv.writer(self.f,delimiter=",")
                writer.writerow([self.i,ser_read_float])
            
            self.i +=1

            if self.stop_threads:
                break

    def done(self):
        self.canvas.get_tk_widget().place_forget()
        self.image_label.place_forget()
        self.controller.switch_frame(DonePage)
        self.controller.title("Results")
        self.done_button.place_forget()
        self.start_button.grid(row=0,column=1)
        
        self.donePage.set_results(self.streamed_data, self.time_per_image, len(self.images))
