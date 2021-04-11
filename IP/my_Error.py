# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 21:25:35 2021

@author: garvi
"""

from PyQt5.QtWidgets import QMessageBox, QInputDialog

#Error.py

class my_Error:
    
    def __init__(self):
        pass
    
    
    def confirm_deletion(self):
   msg = QMessageBox()
   msg.setIcon(QMessageBox.Information)

   msg.setText("This is a message box")
   msg.setInformativeText("This is additional information")
   msg.setWindowTitle("MessageBox demo")
   msg.setDetailedText("The details are as follows:")
   msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
   msg.buttonClicked.connect(msgbtn)
	
   retval = msg.exec_()
   print "value of pressed message box button:", retval
        
        
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

