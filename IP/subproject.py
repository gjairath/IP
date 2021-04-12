# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:16:51 2021

@author: garvi
"""


class SubProject:
    # A sublist is the bottom-most layer.

    def __init__(self, idx):
        self.project_name = "Empty-Project-Name"
        self.name = "Empty-Sub-Task"
        self.idx = idx
        # Members working on this task.
        self.members = 0
        
        # Sp dict holds data like so:
            # person_name: (eta, fin_date)
        
        # The len of this dict is numm_members
        self.sp_dict = {}
        

    def add_data(self, data):
        '''
        Accepts data from the "Add member" button.
                data = [team_member_name, eta, fin_date]
        '''
        self.sp_dict[data[0]] = (data[1], data[2])
        self.members += 1
        
        
        print ("Aded data to: {}\t{}".format(self.name, self.sp_dict))
        
    def edit_data(self, data):
        '''
        Accepts data from gui and basically changes the sp_dict for whichever higher project in charge of this 
                ... bad boy
                
                data = [person_name, eta, fin_Date]
        '''
        is_found = False
        for keys in self.sp_dict:
            if (keys == data[0]):
                self.sp_dict[keys] = (data[1], data[2])
                is_found = True
                
        if (is_found == False):
            return -1
        # Dont change self.members. It's edit.
        print ("Editd data to: {}\t{}".format(self.name, self.sp_dict))
