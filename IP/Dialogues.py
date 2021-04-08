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
        self.new_project_name = QLineEdit()
        self.new_sub_task_name = QLineEdit()
        
        self.layout = QFormLayout()
                
        self.layout.addRow(QLabel("New Project Name:"), self.new_project_name)
        self.layout.addRow(QLabel("Sub-Project Index to change:"), self.comboBox_2)
        self.layout.addRow(QLabel("New Name of this Subtask:"), self.new_sub_task_name)
        
        # indices is a word? Yeah no we speak my english here.
        sub_task_indexes = []
        for subprojects in self.active_project.sub_tasks:
            sub_task_indexes.append(str(subprojects.idx))
            
        self.comboBox_2.clear()
        self.comboBox_2.addItems(sub_task_indexes)

        self.formGroupBox.setLayout(self.layout)
        
    def extract_data(self):
        data = []
        
        # Get the new project name
        i, j = self.layout.getWidgetPosition(self.new_project_name)
        widget_item = self.layout.itemAt(i, j)
        widget = widget_item.widget()
        new_project_name = widget.text()

        # Get the Subtask that needs changing.
        i, j = self.layout.getWidgetPosition(self.comboBox_2)
        widget_item = self.layout.itemAt(i, j)
        widget = widget_item.widget()
        sub_task_to_change = widget.currentText()
        
        # Get the new subproject name
        i, j = self.layout.getWidgetPosition(self.new_sub_task_name)
        widget_item = self.layout.itemAt(i, j)
        widget = widget_item.widget()
        new_sub_task_name = widget.text()
        
        return [new_project_name, sub_task_to_change, new_sub_task_name]
