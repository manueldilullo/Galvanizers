import os
import tkinter as tk
from tkinter import ttk

from utils.db import DB_util

class UserPage(tk.Frame):
    def __init__(self, master, controller, topicPage=None, loginPage=None):
        tk.Frame.__init__(self, master)
        
        self.master = master
        self.controller = controller
        self.topicPage = topicPage
        self.loginPage = loginPage
        
        self.db = DB_util()
        
        # Create the sign out button
        self.signout_btn = tk.Button(self, text="Sign Out", command=self.signOut)
        self.signout_btn.grid(row=0, column=1, sticky="ne", padx=2, pady=2)

        # Create the back button
        self.back_btn = tk.Button(self, text="Back", command=self.goBack)
        self.back_btn.grid(row=0, column=0, sticky="nw", padx=2, pady=2)

        # Set default text label
        self.no_results = tk.Label(self, text=" ")
        self.no_results.grid(row=1, column=0, columnspan=2, pady=50)

        # Create a listbox inside a Frame to display the results
        self.list_frame = tk.Frame(self, bg="white")
        self.list_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        self.listbox = tk.Listbox(self.list_frame, borderwidth=0, bg=self.list_frame.cget('bg'))
        self.listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        list_font = tk.font.Font(family="Arial", size=12)
        self.listbox.configure(font=list_font, selectbackground="lightblue")
        
        # Configure grid weights for the list frame
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)
        
        # Create a scrollbar for the listbox
        self.scrollbar = ttk.Scrollbar(self.list_frame, orient="horizontal", command=self.listbox.xview)
        self.scrollbar.grid(row=1, column=0, sticky="we")
        self.listbox.configure(xscrollcommand=self.scrollbar.set)
        
        self.list_element_padx = 5
        self.list_element_pady = 10

        # Configure the grid to expand the listbox to fill the window
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
    def tkraise(self):
        self.displayResults()
        super().tkraise()
    
    def displayResults(self):
        # Assume you have a function get_user_data(email) that returns a list of results
        results = self.db.get_user_data(self.controller.email)    
        print(results)    
        
        if len(results) == 0:
            self.no_results.config(text="No results found. Take your first measurement before!")
            return

        self.populate_listbox(results)
    
    def populate_listbox(self, results):
        # Populate the listbox with the results
        for result in results:
            result_text_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "results", result[3], f"image{result[4]}.txt")
            with open(result_text_path) as f:
                text_to_show = f"[{result[6]}] {f.read()}"
                
            self.listbox.insert("end", text_to_show.replace("\n"," "))
    
    def setChooseTopicPage(self, topicPage):
        self.topicPage = topicPage
    
    def setLoginPage(self, loginPage):
        self.loginPage = loginPage

    def signOut(self):
        self.clearListbox()
        self.controller.switch_frame(self.loginPage)

    def goBack(self):
        self.clearListbox()
        self.controller.switch_frame(self.topicPage)
        
    def clearListbox(self):
        # Clear the Listbox
        self.listbox.delete(0, tk.END)