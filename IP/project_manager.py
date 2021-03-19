# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 23:18:13 2021

@author: garvi
"""


class Project_Manager:
    # Clementines are better than oranges and if you disagree you're racist.
    
    def __init__(self):

        self.positionx = 0
        self.positiony = 0
        
        # An array that holds tuples of all existing projects. [Created when user clicks new project]
        self.projects = []        
        # A dictionary that holds ctr:button in key-value pairs in a dictionary
        self.existing_project_labels = {}
        
    def add(self, project, window):
        desired_tpl = (project, window, self.positionx, self.positiony)
        self.projects.append(desired_tpl)
        
        self.positiony += 50
        
    def add_label(self, button, button_text):
        # Adds an identifier with each button text, so that its possible to figure out which button is pressed.

        self.existing_project_labels[button_text] = button
        
    def show_all(self):
        print ("Size Now: {}".format(len(self.projects)))
        for values in self.projects:
            print (values[0].name, values[1].project.name)
            print ('\n')
    
        