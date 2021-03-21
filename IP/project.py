# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:01:37 2021

@author: garvi
"""

from subproject import SubProject
import random

class Project:
    # A class/TEMPLATE that holds a new project instance. 
    # It goes like this:
        # Upper layer:          Project.
        # Bottom layer:         Sub-Projects/Tasks.
   
    # For eg:
        # Top Layer:        Do quaterly review.
        # Mid layer:        [1] Assemble balance sheets. [2] Contact the SEC. [3] Set date for invester calls.
    
    # What a sexy sandwich. The bacon is the love of the people that make things happen.
    
    def __init__(self):
        # A new class is made, provide the user with a basic template.
        placeholder = random.randint(1,10000)
        self.name = "Untitled_Project {}".format(placeholder)        
        self.is_active = True                
        empty_sub_task = self.make_sub_project_object()
        self.sub_tasks = []
        self.sub_tasks.append(empty_sub_task)
        self.num_sub_tasks = len(self.sub_tasks)
    
    def make_sub_project_object(self):
        # An object containing sublists
        new_sub_proj = SubProject()        
        return new_sub_proj