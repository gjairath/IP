# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:16:51 2021

@author: garvi
"""

months_array = ["Padding [Unknown]",
          "January",
          "Febuary",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"]

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
                data = [person_name, eta, fin_Date]
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

    def delete_data(self, data):
        '''
        Called from gui.py, onclick.
        data is an array containing all names to delete.
        '''
        
        # I forgot, if u delete and traverse the same dict, it causes problems.
        for names in data:
            del self.sp_dict[names]
            
            # MAN OVERBOARD!
            self.members -= 1
            
        print ("Deleted these names: {}".format(data))
        
        
    def find_key_in_dict(self, data):
        '''
        A Function to find if a key exists in a dictionary,
        
        Params: Data, ideally a name or a string.
        '''
        
        for keys in self.sp_dict:
            if (keys == data):
                return 1
            
        return -1
    
    
    def process_and_return_data(self):
        '''
        Function to process SP data, return it to show in the GUI screen.
        Following same abstraction.
        
        Returns, [total_time_minutes, # members, date-string (the date to finish processed), time-string.]
        '''
        # Total effort in minutes.
        total_effort_left = 0
        for keys in self.sp_dict:
            # sp_dict holds (eta, finish_date)
            # The eta is a string with "Minutes" or "Years" or whatever.
            # Process it first, then check the case.
            
            raw_string = self.sp_dict[keys][0]
            # this split may seem risky but it will always work, this is because how the data is stored first.
            raw_string_array = raw_string.split(' ')
            time_left_int = raw_string_array[0]
            
            # This time_left_int may be something stupid like three hundred or maybe "TOM"
            # isnumeric is good for fault tolerance.
            
            # These values come from the dialog like so:
            #         self.eta_options.addItems(['Minutes', 'Hours', 'Days', 'Months', 'Years'])

            if (time_left_int.isnumeric() == True):
                time_left = int(time_left_int)
                if (raw_string_array[1] == "Years"): 
                    total_effort_left += time_left * 12 * 24 * 24 * 60
                
                elif (raw_string_array[1] == "Months"):
                    # Average the month to 30; 366/12 = 30.50 days in a leap year
                    total_effort_left += time_left * 30 * 24 * 60
                    
                elif (raw_string_array[1] == "Days"):
                    total_effort_left += time_left * 24 * 60
                
                elif (raw_string_array[1] == "Hours"):
                    total_effort_left += time_left * 60
                
                else:
                    total_effort_left += time_left
                    
        from datetime import datetime, timedelta
        eta_from_now = datetime.now() + timedelta(minutes=total_effort_left)
                
        # month is a global array with months
        # This is faster than using stfttime,  
            # def _wrap_strftime(object, format, timetuple):
        # Does lots of checking and other stuff I dont care much about
        
        date_string = str(eta_from_now.day) + " " + str(months_array[eta_from_now.month]) + " " + str(eta_from_now.year)
        time_string = eta_from_now.strftime("%I:%M %p")
        print (date_string, time_string)
        
        return [total_effort_left, self.members, date_string, time_string]

                
