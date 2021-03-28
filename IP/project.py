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
        empty_sub_task = self.make_sub_project_object(placeholder)
        
        # An array of subproject objects. Each has their own data.
        self.sub_tasks = []
        self.sub_tasks.append(empty_sub_task)
        self.num_sub_tasks = len(self.sub_tasks)
        
    def make_sub_project_object(self, idx):
        # An object containing sublists
        new_sub_proj = SubProject(idx)        
        return new_sub_proj
    
    def add_sub_project(self, idx):
        new_sub_proj = SubProject(idx)        
        self.sub_tasks.append(new_sub_proj)
        self.num_sub_tasks = len(self.sub_tasks)

    def display_data(self):
        '''
        Display all data, subprojects/people/ETA's etc.
        '''
        dash = '-' * (len(self.name) + 1)
        ta = self.name + "\n{}\n".format(dash)
        
        for i in range(self.num_sub_tasks):
            string_of_index = "[" +  str(i+1) + "]" + "\t" + "\n"

            string_of_name = "\tName of subtask: \t\t" +  str(self.sub_tasks[i].name) + "\n"
            string_of_members = "\tNumber of Members: \t\t" + str(self.sub_tasks[i].members) + "\n"
            string_of_eta = "\tETA: \t\t\t" + str(self.sub_tasks[i].eta) + "\n"
            string_of_finish_date = "\tFinish_date: \t\t" + str(self.sub_tasks[i].finish_date)
            new_line = "\n"
            
            one_giant_string = string_of_index + string_of_name + string_of_members + string_of_eta \
                                + string_of_finish_date + new_line
            ta += one_giant_string
        
        return ta