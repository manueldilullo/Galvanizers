from .signup_frame import SignupPage
from .login_frame import LoginPage
from .topic_frame import ChooseTopicPage
from .slideshow_frame import SlideshowPage
from .done_frame import DonePage

import os
import json
import tkinter as tk

class App(tk.Tk):
    def __init__(self, isTest):
        tk.Tk.__init__(self)
    
        # Load config file
        self.config = self.load_config_file()
        
        # set title
        self.titlevar = self.config["app"]["titlevar"]
        self.title(self.config["app"]["title"])

        # set windows size
        WINDOW_SIZES = self.config["sizes"]["windows_sizes"]
        RESIZABLE_SIZES = tuple(self.config["sizes"]["resizable_sizes"])
        self.geometry(f"{WINDOW_SIZES[0]}x{WINDOW_SIZES[1]}")
        self.resizable = RESIZABLE_SIZES
        
        # set up container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initialize Frames
        self.frames = {}
        for F in (SignupPage, LoginPage, DonePage):
            self.frames[F.__name__] = F(master=container, controller=self)
            self.frames[F.__name__].grid(row=0, column=0, sticky="nsew")
            
        self.frames[SlideshowPage.__name__] = SlideshowPage(master=container, controller=self, donePage=self.frames[DonePage.__name__], isTest=isTest)
        self.frames[SlideshowPage.__name__].grid(row=0, column=0, sticky="nsew")

        self.frames[ChooseTopicPage.__name__] = ChooseTopicPage(master=container, controller=self, slideShowPage=self.frames[SlideshowPage.__name__])
        self.frames[ChooseTopicPage.__name__].grid(row=0, column=0, sticky="nsew")
        
        self.frames[DonePage.__name__].setChooseTopicPage(ChooseTopicPage)

        self.switch_frame(SignupPage)
        self.title("Signup")

    def switch_frame(self, page_class):
        frame = self.frames[page_class.__name__]
        frame.tkraise()
        
    def load_config_file(self):
        # load config file
        config_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config.json")
        with open(config_filepath) as f:
            config = json.load(f)
        return config