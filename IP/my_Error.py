# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 21:25:35 2021

@author: garvi
"""

from PyQt5.QtWidgets import QMessageBox, QInputDialog

IP_VERSION = "IP Version 2f"

class my_Error:
    #Error.py    
    def __init__(self):
        pass
    
    
    def confirm_deletion(self, name_project, num_sps):
        '''
        Params: name_project is the name of the project that is about to be deleted.
                num_sps      is the number of subprojects in this project.
        '''
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        
        msg.setText("Are you sure you want to delete: \"{}\" with {} sub-projects?".format(name_project, num_sps))
        msg.setWindowTitle(IP_VERSION)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        retval = msg.exec_()
        
        # This OK thing is a macro that is 0x000400 or something.
            # This is because the dialog contains a button in itself, OK and CANCEL.
        if (retval == QMessageBox.Ok):
            return 1
        else:
            return -1
 
        
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

