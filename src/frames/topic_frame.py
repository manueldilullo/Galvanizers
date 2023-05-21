import os
import tkinter as tk
from .slideshow_frame import SlideshowPage

def get_images(folder_name):
    return [os.path.join(folder_name, f) for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]
    
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

        self.slideShowPage.images_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "images", self.master.topic)
        self.slideShowPage.images = get_images(self.slideShowPage.images_folder)
        self.slideShowPage.image_index = 0
        self.slideShowPage.image_label = tk.Label(self.slideShowPage)
        self.slideShowPage.image_label.grid(row=0, column=0)
        
        self.slideShowPage.start_button.grid(row=0,column=1)

        self.controller.switch_frame(SlideshowPage)