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
        # A project may have many sublists.
        # Make a giant string of all of them and simply display it.
        
        
        string_of_name = "Name of subtask: " +  str(self.project.sub_tasks[0].name) + "\n"
        string_of_index = "Index: " +  str(self.project.sub_tasks[0].idx) + "\n"
        string_of_members = "Number of Members:" + str(self.project.sub_tasks[0].members) + "\n"
        string_of_eta = "ETA: " + str(self.project.sub_tasks[0].eta) + "\n"
        string_of_finish_date = "Finish_date: " + str(self.project.sub_tasks[0].finish_date)
        
        one_giant_string = string_of_name + string_of_index + string_of_members + string_of_eta \
                            + string_of_finish_date

        label_giant = QLabel(one_giant_string, self)
        label_giant.resize(250,150)
        label_giant.move(200, 200)