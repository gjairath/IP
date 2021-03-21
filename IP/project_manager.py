# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 23:18:13 2021

@author: garvi
"""

from datetime import datetime


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
        # Adds project in pair-wise tuple to the project managers dictionary.
        desired_tpl = (project, window, self.positionx, self.positiony)
        
        self.projects[button] = desired_tpl
        self.positiony += 35
        
        # Save the state again.
        #self.save_state()

        
    def add_label(self, button, button_text):
        # Adds an identifier with each button text, so that its possible to figure out which button is pressed.
        self.existing_project_labels[button_text] = button
#        self.save_state()
        
    def show_all(self):
        print ("Size Now: {}".format(len(self.projects)))
        print (self.projects)
        print ("\n\n")
        
        
    def save_state(self):
        '''
        A function to save the last state that the user left in, for now it's local.
        '''

        today_date = datetime.now().date()

        fptr_trivial = open("saved_state{}".format(today_date), "wb")
        pickle.dump(self, fptr_trivial)
        
        