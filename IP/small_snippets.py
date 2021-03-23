# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 22:14:33 2021

@author: garvi
"""
import PyQt5

t = [['New Project for lols + 1', PyQt5.QtCore.QRect(0, 35, 121, 23), PyQt5.QtCore.QSize(121, 23), 'button__-1'], ['Wft? + 0', PyQt5.QtCore.QRect(0, 0, 75, 23), PyQt5.QtCore.QSize(75, 23), 'button__0'], ['Wft? + 0', PyQt5.QtCore.QRect(0, 0, 75, 23), PyQt5.QtCore.QSize(75, 23), 'button__1'], ['Wft? + 0', PyQt5.QtCore.QRect(0, 0, 75, 23), PyQt5.QtCore.QSize(75, 23), 'button__2'], ['Wft? + 0', PyQt5.QtCore.QRect(0, 0, 75, 23), PyQt5.QtCore.QSize(75, 23), 'button__3']]


x = [x[0] for x in t]
print (x)


print (set(x))