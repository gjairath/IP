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

    def __init__(self):
        super(Dialog, self).__init__()
        self.createFormGroupBox()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        self.setWindowTitle("Change")
        
    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Project Name")
        layout = QFormLayout()
        
        self.comboBox_2 = QComboBox()
        
        layout.addRow(QLabel("Change Project Name:"), QLineEdit())
        layout.addRow(QLabel("Project Index:"), self.comboBox_2)
        layout.addRow(QLabel("Name:"), QLineEdit())

        list1 = ['1', '2']
        self.comboBox_2.clear()
        self.comboBox_2.addItems(list1)

        self.formGroupBox.setLayout(layout)
        
    def edit_project(self):
        dialog = Dialog()
        dialog.exec_()
