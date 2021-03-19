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
        
        
    def add(self, project, window):
        desired_tpl = (project, window)
        self.projects.append(desired_tpl)
        
        
    def show_all(self):
        print ("Size Now: {}".format(len(self.projects)))
        for values in self.projects:
            print (values[0], values[1])
            print ('\n')
    
        