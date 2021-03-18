# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:49:55 2021

@author: garvi
"""

#gui_helper.py
# Small Description:
    # A host of all dialogs that gui.py invokes FROM ip_main.py

from PyQt5.QtWidgets import QWidget
from project import Project

class New_Project_Window(QWidget):                           
    def __init__(self):
        super().__init__()
        
        # A project object is initialized, that contains various sub-tasks hosts to a TON of information.
            # This should ONLY be done if the new_project button is clicked otherwise why bother?

        #init a new project object
        self.project = Project()
        
        self.setWindowTitle(self.project.name)
        
        
    def display(self):
        # A class to display relevant data
        pass
        