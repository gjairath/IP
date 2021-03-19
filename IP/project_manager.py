# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 23:18:13 2021

@author: garvi
"""


class Project_Manager:
    # Clementines are better than oranges and if you disagree you're racist.
    
    def __init__(self):
        # Update position deltas accordingly.
        self.positionx = 0
        self.positiony = 0
        
        # A dictionary that holds tuples of all existing projects. [Created when user clicks new project]
                # The key here is the button that is shown in the main screen that segues to the new project.
        self.projects = {}        
        
        # A dictionary that holds ctr:button in key-value pairs in a dictionary
        self.existing_project_labels = {}
        
    def add(self, project, window, button):
        desired_tpl = (project, window, self.positionx, self.positiony)
        
        self.projects[button] = desired_tpl
        self.positiony += 35
        
    def add_label(self, button, button_text):
        # Adds an identifier with each button text, so that its possible to figure out which button is pressed.
        self.existing_project_labels[button_text] = button
        
    def show_all(self):
        print ("Size Now: {}".format(len(self.projects)))
        print (self.projects)
        print ("\n\n")
        