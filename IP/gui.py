# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:10:34 2021

@author: garvi
"""

import sys
import gui_helper as gui_h

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDesktopWidget, QLabel
from PyQt5.QtGui import QIcon

from project import Project

class Main_Screen(QWidget):
    #not the best name for a class but honestly I cant think without this
    
    def __init__(self, project_manager):
        super().__init__()
        self.title = "TESTING-MODEL-0"
        
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
 
        self.add_new_project_button()
        self.init_UI()
                
        # self indicates the screen moving to the center here self is the class object.
        self.center_object(self)
        
        
        self.manager = project_manager
        
        # A counter to track the projects, it helps to show which window to display.
        self.counter = -1
        
        
    def center_object(self, desired_object):
        """
        Parameters
        ----------
        desired_object : object to center
                       This function centers an object on to the desktop screen NOT the screen's screen.

        Returns
        -------
        None.
        """
                

        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()

        qtRectangle.moveCenter(centerPoint)
        desired_object.move(qtRectangle.topLeft())
        
    def init_UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
    
    
    def show_appropriate_window(self):
        """
        This function shows the appropriate window for whatever project.
        So if a user creates 10 projects, the 5th button shows the 5th window.
        
        The project manager contains all the existing projects as an object.
            It contains an array called projects which has pair-wise tuples of:
                    (project, window)
        
        Returns: Void
        """
        
        
        self.manager.projects[self.counter][1].show()
        
        
    
    def new_project_window(self):                
        """
        Event that a new project button is clicked. 
        Create a new project, update relevant stuff.
                            
        Returns: Void.
        """
        
        # Make a brand new project template.
        new_project = Project()

        # Make a brand new window.
        new_window = gui_h.New_Project_Window(new_project)
        new_window.show()

        # Make a brand new button.        
        new_exisiting_project_btn = QPushButton("Testing + {}".format(self.counter), self)
        
        # Adjust the positions of the new project labels.
        self.tracker = 1
        new_exisiting_project_btn.move(self.tracker,self.tracker)
        self.tracker += 5
        
        new_exisiting_project_btn.clicked.connect(self.show_appropriate_window) 
        new_exisiting_project_btn.show()
        
        # Add the appropriate values to the project manager class object.
        self.manager.add(new_project, new_window)
        
        # Just debugging here.
        self.manager.show_all()
        
        
        # Finally, increment the total tally of projects existing.
        self.counter += 1
    
    def add_new_project_button(self):
        """
        Adds the "new project" button on to the screen
        Returns
        -------
        None.
        """
        
        new_project_btn = QPushButton("New Project", self)
        new_project_btn.resize(250,150)
        new_project_btn.clicked.connect(self.new_project_window) 
        
    
        new_project_btn.move(200, 200)
        
    def debug(self):
        print("Click me harder!")