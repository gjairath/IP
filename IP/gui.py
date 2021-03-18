# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:10:34 2021

@author: garvi
"""

import sys
import gui_helper as gui_h

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDesktopWidget, QLabel
from PyQt5.QtGui import QIcon


class Main_Screen(QWidget):
    #not the best name for a class but honestly I cant think without this
    
    def __init__(self):
        super().__init__()
        self.title = "TESTING-MODEL-0"
        
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
 
        self.add_new_project_w()
        self.init_UI()
                
        # self indicates the screen moving to the center here self is the class object.
        self.center_object(self)
        
        

        
    def center_object(self, desired_object):
        # A function to center my screen to the screen of the person, hopefully works cross-os
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()

        qtRectangle.moveCenter(centerPoint)
        desired_object.move(qtRectangle.topLeft())
        
    def init_UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
    
    def new_project_window(self):                

        # Creates a new dialog, that is, a new project window since new project button is clicked.                             
        self.dialog = gui_h.New_Project_Window() 
        self.dialog.show()
        #self.dialog.hide()
    
    def add_new_project_w(self):
        
        # A button to add a new project
        new_project_btn = QPushButton("New Project", self)
        new_project_btn.resize(250,150)
        new_project_btn.clicked.connect(self.new_project_window) 
        
    
        new_project_btn.move(200, 200)
        
    def debug(self):
        print("Click me harder!")