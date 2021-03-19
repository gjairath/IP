# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:16:51 2021

@author: garvi
"""


class SubList:
    # A sublist is the bottom-most layer.
    
    def __init__(self):
        self.name = "Empty-Sub-Task"
        
        # Members working on this task.
        self.members = 1
        
        # Eta for this task in minutes.
        self.eta = str(0) + " Minutes"
        
        # The finish date for this project
        self.finish_date = "01/01/2099"
        
        
        self.idx = 1