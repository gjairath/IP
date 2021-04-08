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
        self.new_sub_task_members = QLineEdit()
        self.new_sub_task_ETA = QLineEdit()
        #self.new_sub_task_finish_date = 
        
        
        self.layout = QFormLayout()
                
        self.layout.addRow(QLabel("New Project Name:"), self.new_project_name)
        # This is like a new line, im really smart lol.
        self.layout.addRow(QLabel(""))
        
        self.layout.addRow(QLabel("Sub-Project Index to change:"), self.comboBox_2)
        self.layout.addRow(QLabel("New Name of this Subtask:"), self.new_sub_task_name)
        self.layout.addRow(QLabel("New Members of this Subtask:"), self.new_sub_task_members)
        self.layout.addRow(QLabel("New ETA this Subtask:"), self.new_sub_task_ETA)

        # indices is a word? Yeah no we speak my english here.
        sub_task_indexes = []
        for subprojects in self.active_project.sub_tasks:
            sub_task_indexes.append(str(subprojects.idx))
            
        self.comboBox_2.clear()
        self.comboBox_2.addItems(sub_task_indexes)



        self.new_project_name.setPlaceholderText(self.active_project.name)
        self.new_sub_task_name.setPlaceholderText("Name of Subtask")
        self.new_sub_task_members.setPlaceholderText("1")
        self.new_sub_task_ETA.setPlaceholderText("ETA Of Subtask")

        self.formGroupBox.setLayout(self.layout)
        
        
    def extract_qline(self, widget_name):
        '''
        I vowed not to deduplicate this time.
        '''
        i, j = self.layout.getWidgetPosition(widget_name)
        widget_item = self.layout.itemAt(i, j)
        widget = widget_item.widget()
        
        return widget.text()
    
    def extract_qbox(self, widget_name):
        i, j = self.layout.getWidgetPosition(self.comboBox_2)
        widget_item = self.layout.itemAt(i, j)
        widget = widget_item.widget()
        
        return widget.currentText()
        
    def extract_data(self):        
        # Get the new project name
        new_project_name = self.extract_qline(self.new_project_name)
        new_sub_task_name = self.extract_qline(self.new_sub_task_name)
        new_sub_task_members = self.extract_qline(self.new_sub_task_members)
        new_sub_task_ETA = self.extract_qline(self.new_sub_task_ETA)        
        # Get the Subtask that needs changing.
        sub_task_to_change = self.extract_qbox(self.comboBox_2)
        
        return [new_project_name, sub_task_to_change, new_sub_task_name, new_sub_task_members, new_sub_task_ETA]
