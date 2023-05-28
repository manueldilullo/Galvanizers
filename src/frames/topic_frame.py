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
        
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 3), weight=1)
        
        self.topic_label = tk.Label(self, text="Choose a topic:")
        self.topic_label.grid(row=1, column=0, sticky="e")

        self.topics = ["Dogs", "Superheroes", "Flowers"]
        self.topic_var = tk.StringVar()
        self.topic_var.set(self.topics[0])
        self.topic_dropdown = tk.OptionMenu(self, self.topic_var, *self.topics)
        self.topic_dropdown.grid(row=1, column=1, sticky="w")

        self.done_button = tk.Button(self, text="Done", command=self.done)
        self.done_button.grid(row=2, column=0, columnspan=2)

    def done(self):
        self.master.topic = self.topic_var.get()
        self.slideShowPage.topic = self.master.topic
        self.slideShowPage.controller.title("Slideshow " + self.slideShowPage.topic)
        self.slideShowPage.msg.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        self.slideShowPage.images_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "images", self.master.topic)
        print(self.slideShowPage.images_folder)
        self.slideShowPage.images = get_images(self.slideShowPage.images_folder)
        self.slideShowPage.image_index = 0
        self.slideShowPage.image_label = tk.Label(self.slideShowPage)
        self.slideShowPage.image_label.place(relx=0.35, rely=0.5, anchor=tk.E)
        
        self.slideShowPage.start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.controller.switch_frame(SlideshowPage)
