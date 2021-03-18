# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:01:37 2021

@author: garvi
"""

from sublist import SubList

class Project:
    # A class that holds a new project instance. 
    # A project object contains subtasks which hold "to-do lists" with whatever people.
    
    def __init__(self):
        # A new class is made, provide the user with a basic template.
        
        self.name = "Untitled_Project"
        self.is_active = True
        
        
        empty_sub_task = self.make_sub_list()
        self.sub_tasks = []
        self.sub_tasks.append(empty_sub_task)
        
        self.num_sub_tasks = len(self.sub_tasks)
        
    
    def make_sub_list(self):
        # An object containing sublists
        new_sub_list = SubList()
        
        return new_sub_list
        
    