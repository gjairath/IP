# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 01:43:40 2021

@author: garvi
"""

from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout)


class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, active_project):
        super(Dialog, self).__init__()
        self.active_project = active_project
 
        self.createFormGroupBox()
                
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        self.setWindowTitle("Change Project - {}".format(self.active_project.name))
        
    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("{}".format(self.active_project.name))
    
        self.comboBox_2 = QComboBox()

        layout = QFormLayout()
                
        layout.addRow(QLabel("Change Project Name:"), QLineEdit())
        layout.addRow(QLabel("SubProject Index to change:"), self.comboBox_2)
        layout.addRow(QLabel("Name:"), QLineEdit())
        
        # indices is a word? Yeah no we speak my english here.
        sub_task_indexes = []
        for subprojects in self.active_project.sub_tasks:
            sub_task_indexes.append(str(subprojects.idx))
            
        self.comboBox_2.clear()
        self.comboBox_2.addItems(sub_task_indexes)

        self.formGroupBox.setLayout(layout)
        
    def edit_project(self, active_project):
        
        dialog = Dialog(active_project)
        dialog.exec_()
