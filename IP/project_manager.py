# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 23:18:13 2021

@author: garvi
"""

class Project_Manager:        
    def __init__(self):
        # Projects:             A Dictionary that contains {button: (projects, window, x, y)}
        #                       Helps to retain data between sessions.
        
        # Existing_Labels:      A Dictionary that contains {button: button_text}
        #                       Helps to segue the windows appropriately.
        
        self.positionx = 0
        self.positiony = 0
        
        self.projects = {}        
        self.existing_project_labels = {}
        
    def add(self, project, window, button):
        '''
        Params: 
            Project - A Project object, basically the main projects/tasks.
            Window - The GUI window LINKED with each project that shows sub-projects/data/people/ETA etc..
            Button - The button that toggles the display.
        
        Description:
            adds a tuple to the dictionary projects [see init]
        '''
        desired_tpl = (project, window, self.positionx, self.positiony)
        
        self.projects[button] = desired_tpl
        self.positiony += 35
        

    def add_label(self, button, button_text):
        '''
        Params:
            button - each button that toggles the project windows.
            button_text - identifier to actually find the button.
            
        Description:
            Adds the tuples to the existing_labels dictionary [see init]
        '''
        self.existing_project_labels[button_text] = button
        
    def show_all(self):
        '''
        Mostly for debugging purposes.
        '''
        print ("Size Now: {}".format(len(self.projects)))
        print (self.projects)
        print ("\n\n")        