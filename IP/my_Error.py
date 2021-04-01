# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 21:25:35 2021

@author: garvi
"""

from PyQt5.QtWidgets import QMessageBox

#Error.py

class my_Error:
    
    def __init__(self):
        pass
    
    
    
    def add_a_project(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('Add a project first!')
        msg.setWindowTitle("Error")
        msg.exec_()
        
        
    def click_button_first(self):
        '''
        If you try moving a button without clicking it, it will cause an error.
        '''
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('Click on a button before moving it first!')
        msg.setWindowTitle("Error")
        msg.exec_()

