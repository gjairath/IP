# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:16:51 2021

@author: garvi
"""


class SubProject:
    # A sublist is the bottom-most layer.

    def __init__(self, idx):
        self.name = "Empty-Sub-Task"
        self.idx = idx
        # Members working on this task.
        self.members = 1
        # Eta for this task in minutes.
        self.eta = str(0) + " Minutes"
        # The finish date for this project
        self.finish_date = "01/01/2099"


    def display_data(self):
        '''
        Display all data, subprojects/people/ETA's etc.
        '''
        string_of_index = "[" +  str(self.idx) + "]\n"
        string_of_name = "\tName of subtask: \t\t" +  str(self.name) + "\n"
        string_of_members = "\tNumber of Members: \t\t" + str(self.members) + "\n"
        string_of_eta = "\tETA: \t\t\t" + str(self.eta) + "\n"
        string_of_finish_date = "\tFinish_date: \t\t" + str(self.finish_date)
        
        one_giant_string = string_of_index + string_of_name + string_of_members + string_of_eta \
                            + string_of_finish_date

        return one_giant_string
