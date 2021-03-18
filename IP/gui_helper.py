# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:49:55 2021

@author: garvi
"""

#gui_helper.py
# Small Description:
    # A host of all dialogs that gui.py invokes FROM ip_main.py

from PyQt5.QtWidgets import QWidget, QLabel
from project import Project

class New_Project_Window(QWidget):                           
    def __init__(self):
        super().__init__()
        
        # A project object is initialized, that contains various sub-tasks hosts to a TON of information.
            # This should ONLY be done if the new_project button is clicked otherwise why bother?

        #init a new project object
        self.project = Project()
        
        self.setWindowTitle(self.project.name)
        
        self.display_data()
        
        
    def display_data(self):
        
        # A button to add a new project
        string_of_members = "Number of Members:" + str(self.project.sub_tasks[0].members)
        label_members = QLabel(string_of_members, self)
        label_members.resize(250,150)
        label_members.move(200, 200)
        
        string_of_eta = "ETA: " + str(self.project.sub_tasks[0].eta)
        string_of_eta = QLabel(string_of_eta, self)
        string_of_eta.resize(250,150)
        string_of_eta.move(300, 300)

        