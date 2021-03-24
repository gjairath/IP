# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:49:55 2021

@author: garvi
"""

#gui_helper.py
# Small Description:
    # A host of all dialogs that gui.py invokes FROM ip_main.py

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget, QPushButton
from project import Project

class New_Project_Window(QWidget):       
    # A supermodel who shows the lottery numbers, she's irrelevant, the numbers are not.
    def __init__(self, new_project):
        '''
        Params:
            New_project - A Project() Object for a newly created object.
            
        Desc:
            Makes a new project window.
        '''
        super().__init__()        
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        #init a new project object
        self.project = new_project
        
        self.setWindowTitle(self.project.name)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center_object(self)
        
    def display_data(self):
        '''
        Display all data, subprojects/people/ETA's etc.
        '''
        string_of_index = "[" +  str(self.project.sub_tasks[0].idx) + "]" + "\t" + str(self.project.sub_tasks[0].project_name) + "\n\n"
        string_of_name = "\tName of subtask: \t\t" +  str(self.project.sub_tasks[0].name) + "\n"
        string_of_members = "\tNumber of Members: \t\t" + str(self.project.sub_tasks[0].members) + "\n"
        string_of_eta = "\tETA: \t\t\t" + str(self.project.sub_tasks[0].eta) + "\n"
        string_of_finish_date = "\tFinish_date: \t\t" + str(self.project.sub_tasks[0].finish_date)
        
        one_giant_string = string_of_index + string_of_name + string_of_members + string_of_eta \
                            + string_of_finish_date

        label_giant = QPushButton(one_giant_string, self)
        # Do adjust size instead, its cleaner.
        label_giant.adjustSize()        

        return one_giant_string    
    
    def center_object(self, desired_object):
        # A function to center my screen to the screen of the person, hopefully works cross-os
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()
        qtRectangle.moveCenter(centerPoint)
        desired_object.move(qtRectangle.topLeft())