# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 04:06:58 2021

@author: garvi
"""


def get_sp_graph(name_array, tuple_data_array):
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
    for idx, value in enumerate(tuple_data_array):
        num_hours = value[0].split(' ')[0]
        if (num_hours.isnumeric()):
            hour_data_for_names.append(int(num_hours) / 60)
            new_name_data.append(name_array[idx])
    
    
    hours_left = 673 / 60        
    print (hour_data_for_names, new_name_data, hours_left)
    
    # Free memory    
    name_array.clear()
    tuple_data_array.clear()
    
    import matplotlib.pyplot as plt
    # Pie chart
    labels = ['Frogs', 'Hogs', 'Dogs', 'Logs']
    sizes = [15, 30, 45, 10]
    #colors
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
     
    fig1, ax1 = plt.subplots()
    ax1.pie(hour_data_for_names, colors = colors, labels=new_name_data, autopct='%1.1f%%', startangle=90)
    
    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc='lightgrey')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    fig.set_facecolor('lightgrey')
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')  
    plt.tight_layout()
    
    
    return fig
