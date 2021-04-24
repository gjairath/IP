# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 04:06:58 2021

@author: garvi
"""

import matplotlib.pyplot as plt
import numpy as np

max_string = 1

def reinit(data):
    # Data is (eta, fin date) array
    
    # This will have days, months, years, hours.
    # Or maybe less.
    global max_string
    
    set_vals = set()
    for idx, x in enumerate(data):
        first_value = x[0].split(" ")
        hour_value = first_value[1]
        set_vals.add(hour_value)
   
    if ("Years" in set_vals):
        max_string = 4
    elif ("Months" in set_vals):
        max_string = 3
    elif ("Days" in set_vals):
        max_string = 2
    elif ("Hours" in set_vals):
        max_string = 1
    else:
        max_string = 0
    
    return max_string

def conv_to_hours(random_time, random_time_mode):
    '''
    A utility function to convert data and set a max string.
    '''
    global max_string

    ret = 0
    if (random_time_mode == "Years"): 
        ret += random_time * 365 * 24
        
    elif (random_time_mode == "Months"):
    # Average the month to 30; 366/12 = 30.50 days in a leap year
        ret += random_time * 730.001
        
    elif (random_time_mode == "Days"):
        ret += random_time * 24
        
    elif (random_time_mode == "Hours"):
        ret += random_time
        
    else:
        ret += random_time / 60
        
    return ret


def convert_max_string_to_string(max_s, total_hours):
    '''
    The title on the piechart corresponds to the Maximum time taken by any member.
    
    So if X takes 3 years, the total time and the "years" tag will be displayed.
    '''
    
    ret = "Hours"
    if (max_s == 4):
        ret = "Years"
        total_hours = total_hours / 8760
    elif (max_s == 3):
        ret = "Months"
        total_hours = total_hours / 730.001
    elif (max_s == 2):
        ret = "Days"
        total_hours = total_hours / 24
    elif (max_s == 1):
        ret = "Hours"
    else:
        ret = "Hours"

    return ret, total_hours

def get_sp_graph(name_array, tuple_data_array, effort_last):
    '''
    This graphs the SP time left and member data.
    
    name_array: Array of names of members.
    tuple_data_array: The values in the sp_dict related to these names.
    
    The data will not alway sbe processed, it will be raw and stupid. 
    Process it first and return a figure instance.
    
    Returns: Fig instance.
    '''
    
    max_string = reinit(tuple_data_array)
    
    hour_data_for_names = []
    new_name_data = []
    bad_data = []
    total_hours = 0.0
    
    for idx, value in enumerate(tuple_data_array):
        # value is basically an array of values related to keys in sp_dict.
        # value = [(eta, fin_date), (eta2, fin_date2)] etc..
        
        tuple_string = value[0].split(' ')
        random_time = tuple_string[0]
        
        if (random_time.isnumeric()):
            # The array comes in like this: ['3 hours', '3 years', '4 days']   
            num_hours = conv_to_hours(float(random_time), tuple_string[1])
            total_hours += num_hours
            
            hour_data_for_names.append((float(num_hours)) * (100 / effort_last))
            new_name_data.append(name_array[idx])
            
        else:
            # If the name of a member in the SP lacks a number BEFORE the hour/year/days tag, do this.
            bad_data.append(name_array[idx])
    
    bad_data_example = ""
    is_bad_data = False
    if (len(bad_data) != 0):
        is_bad_data = True
        bad_data_example = bad_data[0]
        
    # Free memory    
    name_array.clear()
    tuple_data_array.clear()
    
    # Pie chart

    #colors
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
     
    fig1, ax1 = plt.subplots() 
        
    ax1.pie(hour_data_for_names, colors = colors, startangle=90)


    #draw circle
    centre_circle = plt.Circle((0,0),0.8,fc='lightgrey')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    fig.set_facecolor('lightgrey')
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    
    # This is stupid, it basically toggles the title based on max time.
    # So, if X and Y are members with time say 5 minutes an 3 hours, the title must show ~ 3 hours.
    
    # It also shows which members data is being omitted, since user might enter dumb data.
    
    plt.axis('equal')
    if (is_bad_data == False):
        if (effort_last <= 0):
            plt.title("Less than an hour left", fontsize = 'small')
        else:
            
            max_time, max_value = convert_max_string_to_string(max_string, total_hours)
            plt.title("Total {} ~ {:.0f} {}" \
                      .format(max_time, max_value, max_time), fontsize = 'small')
            
            
    else:
        plt.title("Total Hours ~ {:.0f} Hours ({} has no ETA; It's omitted.)" \
                  .format(effort_last, bad_data_example),
                  fontsize = 'small')
        
    new_arr = []
    for idx, value in enumerate(new_name_data):
        new_arr.append(str(new_name_data[idx]) + " (" + str(int(hour_data_for_names[idx])) + "%)")
        
    plt.legend(labels = new_arr, fontsize = 'small', loc = 'center', prop={'size': 10})

    plt.tight_layout()
    
    return fig
