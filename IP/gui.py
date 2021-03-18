# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:10:34 2021

@author: garvi
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDesktopWidget, QLabel
from PyQt5.QtGui import QIcon


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "TESTING-MODEL-0"
        
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        
        self.layout        
        self.init_UI()
        
        # self indicates the screen moving to the center here self is the class object.
        self.center_object(self)
        

    def center_object(self, desired_object):
        # A function to center my screen to the screen of the person, hopefully works cross-os
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()

        qtRectangle.moveCenter(centerPoint)
        desired_object.move(qtRectangle.topLeft())
        
    def init_UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

        
    def debug(self):
        print("Click me harder!")
        
        
    def show_dialogs(self, object_to_show):
        object_to_show.show()
