# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 22:14:33 2021

@author: garvi
"""
import pickle

dict_project = {1: (1,2,3,4), 2:(1,6,3,4)}
new_dict = {}

i = 1
for key in dict_project.copy():
    # Take existing dict with a mapping and replace it with a placeholder.
    new_dict["button__{}".format(i)] = dict_project[key]
    
    # Let garbage collector dereference this
    del dict_project[key]
    
    i += 1
    

pickle.dump(new_dict, open("subproj.dat", "wb"))

sex = pickle.load(open("subproj.dat", "rb"))

print (sex)