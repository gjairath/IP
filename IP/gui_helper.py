# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:49:55 2021

@author: garvi
"""

#gui_helper.py
# Small Description:
    # A host of all dialogs that gui.py invokes FROM ip_main.py

from PyQt5.QtWidgets import QWidget

class New_Project_Window(QWidget):                           
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PUT-NAME-HERE-PROJECT")
        
        
    def display(self):
        # A class to display relevant data
        pass
        