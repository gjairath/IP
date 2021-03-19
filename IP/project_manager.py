# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 23:18:13 2021

@author: garvi
"""


class Project_Manager:
    # Clementines are better than oranges and if you disagree you're racist.
    
    def __init__(self):
        
        # An array that holds tuples of all existing projects. [Created when user clicks new project]
        self.projects = []
        self.position = 10
        
        
        self.existing_project_labels = []
        
    def add(self, project, window):
        desired_tpl = (project, window, self.position)
        self.projects.append(desired_tpl)
        
        self.position += 50
        
    def add_label(self, ctr, button):
        # This adds labels that you see on the main screen once the user clicks "New Project"
        desired_tpl = (ctr, button)
        
        # The pair-wise tuple here is in the form, identifier - label.
        self.existing_project_labels.append(desired_tpl)
        
    def show_all(self):
        print ("Size Now: {}".format(len(self.projects)))
        for values in self.projects:
            print (values[0].name, values[1].project.name)
            print ('\n')
    
        