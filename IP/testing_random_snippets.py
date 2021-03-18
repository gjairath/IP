# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:10:34 2021

@author: garvi
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDesktopWidget
from PyQt5.QtGui import QIcon

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "TESTING-MODEL-0"
        
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        
        self.add_widgets()
        self.init_UI()
        self.center_object()
        
    def add_widgets(self):
        layout = QVBoxLayout()
        
        # A button to add a new project
        new_project_button = QPushButton("New Project")
 
        layout.addWidget(new_project_button)
 
        self.setLayout(layout)

    def center_object(self):
        # A function to center my screen to the screen of the person, hopefully works cross-os
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()

        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
    def init_UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = App()
    sys.exit(app.exec_())

