# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 22:14:33 2021

@author: garvi
"""
import PyQt5

t = [['fuck new porject + 0', 'PyQt5.QtCore.QRect(0, 0, 100, 30)', 'PyQt5.QtCore.QSize(100, 30)', 'button__-1']]



button_name = t[0][3]
button_id = (button_name[len("button__"):])

print (int(button_id))
# The way this works is that its basically sorted in order, I dont need button name, but it helps to have anyway.

something = PyQt5.QtCore.QRect(0, 0, 100, 30)

print (something.x())