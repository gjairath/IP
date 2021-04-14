# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 04:06:58 2021

@author: garvi
"""


def get_sp_graph(name_array, tuple_data_array, effort_last):
    '''
    This graphs the SP time left and member data.
    
    name_array: Array of names of members.
    tuple_data_array: The values in the sp_dict related to these names.
    
    The data will not alway sbe processed, it will be raw and stupid. 
    Process it first and return a figure instance.
    
    Returns: Fig instance.
    '''
    
    hour_data_for_names = []
    new_name_data = []
    hours_left = effort_last / 60        
    bad_data = []
    
    for idx, value in enumerate(tuple_data_array):
        num_hours = value[0].split(' ')[0]
        if (num_hours.isnumeric()):
            # This is notn complex, it's ust matply divides by 100, I want it to divide by my total instead.
            # I know I can use autopct but that was glitchingn out on me so this seemd more cleaner I guess.
            hour_data_for_names.append((int(num_hours) / 60) * (100 / hours_left))
            new_name_data.append(name_array[idx])
        else:
            bad_data.append(name_array[idx])
    
    bad_data_example = ""
    is_bad_data = False
    if (len(bad_data) != 0):
        is_bad_data = True
        bad_data_example = bad_data[0]
        
    # Free memory    
    name_array.clear()
    tuple_data_array.clear()
    
    import matplotlib.pyplot as plt
    # Pie chart

    #colors
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
     
    fig1, ax1 = plt.subplots() 
    ax1.pie(hour_data_for_names, colors = colors, labels=new_name_data, autopct='%1.1f%%', pctdistance=0.8, \
            textprops={'fontsize': 6}, startangle=90)

    #draw circle
    centre_circle = plt.Circle((0,0),0.8,fc='lightgrey')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    fig.set_facecolor('lightgrey')
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')
    if (is_bad_data == False):
        plt.title("Total Hours ~ {:.0f} Hours".format(hours_left), fontsize = 'small')
    else:
        plt.title("Total Hours ~ {:.0f} Hours ({} has no ETA; It's omitted.)".format(hours_left, bad_data_example), \
                  fontsize = 'small')
        
    plt.legend(new_name_data, fontsize = 'small', loc = 'center', prop={'size': 6})
    plt.tight_layout()
    
    
    return fig
