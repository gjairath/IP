# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:49:55 2021

@author: garvi
"""

#gui_helper.py
# Small Description:
    # Mainly exists to draw a bridge between the data and the gui, 
    # The data is what project/sublist holds.
    # The gui is simply a screen, with the very basics, that way everything is safely abstracted away.

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout


class Window2(QWidget):                           
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PUT-NAME-HERE-PROJECT")
        
        
    def display(self):
        # A class to display relevant data
        pass
        
def window2():                                             
    w = Window2()
    w.show()

def add_widgets():
    
    # A button to add a new project
    new_project_btn = QPushButton("New Project")
    new_project_btn.resize(250,150)
    new_project_btn.clicked.connect(window2) 
    

    new_project_btn.move(200, 200)
    
    return new_project_btn


def complete_widgets(widget_array):
    layout = QVBoxLayout()
    
    for widget in widget_array:
        layout.addWidget(widget)
        
    return layout