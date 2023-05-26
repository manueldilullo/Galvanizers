import os
import tkinter as tk
from numpy import mean

from PIL import Image, ImageTk

from utils.db import DB_util
from utils.smtp import SMTP_util

class DonePage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        
        self.smtp = SMTP_util() 
        self.db = DB_util()
        
        self.max_val = tk.Label(self, text=" ")
        self.max_val.pack(pady=50)

        self.results = tk.Label(self, text=" ")
        self.results.pack(pady=50)

        self.image_label = tk.Label(self)
        self.image_label.pack(pady=45)

        self.email_button = tk.Button(self, text="Send me an email", command=self.send_email)
        self.email_button.pack(pady=10)
        
        self.done_button = tk.Button(self, text="Done", command=self.done)
        self.done_button.pack(pady=10)
    
    def setChooseTopicPage(self, chooseTopicPage=None):
        self.chooseTopicPage = chooseTopicPage
        
    def set_results(self, streamed_data, time_per_image, n_images):
        averages = []
        
        range_size = time_per_image/100
        for limit in range(n_images): 
            lower_limit = int(limit * range_size)
            upper_limit = int((limit + 1) * range_size)
            print(f"Limitsss {lower_limit}, {upper_limit}")
            averages.append(mean(streamed_data[lower_limit:upper_limit]))

        max_average = max(averages)
        max_average_index = str(averages.index(max_average)+1) 
        
        text = f"The image you have reacted the most to is the # {max_average_index} with average gsr value equal to {max_average}"
        self.max_val.config(text=text)
        
        
        self.images_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "images", self.master.topic)
        img_path =  os.path.join(self.images_folder, f"image{max_average_index}.jpg")

        self.result_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "results", self.master.topic)
        result_path =  os.path.join(self.result_folder, f"image{max_average_index}.txt")

        with open(result_path) as f:
            results = f.read()
        self.results.config(text=results)
        
        image_bin = Image.open(img_path)
        image_bin.thumbnail(tuple(self.controller.config["sizes"]["image_sizes"]), Image.Resampling.LANCZOS)

        self.img = ImageTk.PhotoImage(image_bin)
        self.image_label.config(image=self.img)
    
    def send_email(self):
        # TODO IMPLEMENT THIS
        # to_address = self.db.get_email()
        # self.smtp.send_email()
        print("Not implemented yet")
        pass

    def done(self):
        self.done_button.grid_remove()
        self.controller.switch_frame(self.chooseTopicPage)
        self.controller.title("Choose Topic")
