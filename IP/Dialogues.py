# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 01:43:40 2021

@author: garvi
"""

from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout)


# Lol I wrote this i forgot what it does.
# NOte to self: This is the dialog class for "EDIT PROJECT"

class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, active_project, default = True):
        super(Dialog, self).__init__()
        self.active_project = active_project
 
        if (default == True):
            # To avoid de duplication, this smae code block is reused when a user adds team members to SPs
            # for a given project.
            
            # Define SP: Sub-project
            self.create_group_box()    
        else:
            self.create_group_box_add_members()
                
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(btn_box)
        self.setLayout(main_layout)
        
        self.setWindowTitle("Change Project - {}".format(self.active_project.name))
        
    def create_group_box_add_members(self):
        '''
        Does exactly the same as below but for adding members to a SP.
        '''
        self.form_group_box = QGroupBox("{}".format(self.active_project.name))
        
        self.team_member_name = QLineEdit()
        self.eta = QLineEdit()
        self.fin_date = QLineEdit()

        self.layout = QFormLayout()

        self.layout.addRow(QLabel("New Team-Member Name:"), self.team_member_name)
        self.layout.addRow(QLabel("New ETA:"), self.eta)
        self.layout.addRow(QLabel("New Finish Date:"), self.fin_date)

        self.team_member_name.setPlaceholderText("Name of Member")
        self.eta.setPlaceholderText("ETA Of Subtask")
        self.fin_date.setPlaceholderText("01/01/2022")

        self.form_group_box.setLayout(self.layout)
        
    def create_group_box(self):
        self.form_group_box = QGroupBox("{}".format(self.active_project.name))
    
        self.comboBox_2 = QComboBox()
        self.new_project_name = QLineEdit()
        self.new_sub_task_name = QLineEdit()
        
        
        self.layout = QFormLayout()
                
        self.layout.addRow(QLabel("New Project Name:"), self.new_project_name)
        # This is like a new line, im really smart lol.
        self.layout.addRow(QLabel(""))
        
        self.layout.addRow(QLabel("Sub-Project Index to change:"), self.comboBox_2)
        self.layout.addRow(QLabel("New Name of this Subtask:"), self.new_sub_task_name)

        # indices is a word? Yeah no we speak my english here.
        sub_task_indexes = []
        for subprojects in self.active_project.sub_tasks:
            sub_task_indexes.append(str(subprojects.idx))
            
        self.comboBox_2.clear()
        self.comboBox_2.addItems(sub_task_indexes)



        self.new_project_name.setPlaceholderText(self.active_project.name)
        self.new_sub_task_name.setPlaceholderText("Name of Subtask")

        self.form_group_box.setLayout(self.layout)
        
        
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
        # Get the Subtask that needs changing.
        sub_task_to_change = self.extract_qbox(self.comboBox_2)
        
        return [new_project_name, sub_task_to_change, new_sub_task_name]


    def extract_sp_data(self):
        '''
        A function like above, but extract SP data.
        '''
        team_member_name = self.extract_qline(self.team_member_name)
        eta = self.extract_qline(self.eta)
        fin_date = self.extract_qline(self.fin_date)

        return [team_member_name, eta, fin_date]