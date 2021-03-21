# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 22:04:17 2021

@author: garvi
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:10:34 2021

@author: garvi
"""

import sys
import gui_helper as gui_h

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDesktopWidget, QLineEdit, QInputDialog
from PyQt5.QtGui import QIcon

from project import Project

import testing_random_snippets as ta

class Main_Screen(ta.QMainWindow):
    #not the best name for a class but honestly I cant think without this
    
    def __init__(self, project_manager, parent = None):
        super(Main_Screen, self).__init__(parent)
      #  self._gui_restore()
            
        self.title = "TESTING-MODEL-1c (First version was 0a)"
        
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
 
        self.add_new_project_button()
        self.init_UI()
                
        # self indicates the screen moving to the center here self is the class object.
        self.center_object(self)
        
        
        self.manager = project_manager
        
        # A counter to track the projects, it helps to show which window to display.
        self.counter = -1
        
        
    def center_object(self, desired_object):
        """
        Parameters
        ----------
        desired_object : object to center
                       This function centers an object on to the desktop screen NOT the screen's screen.

        Returns
        -------
        None.
        """
                

        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()

        qtRectangle.moveCenter(centerPoint)
        desired_object.move(qtRectangle.topLeft())
        
    def init_UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.show()
        
        
    def get_text(self):
        
        dlg =  QInputDialog(self)                 
        dlg.setInputMode( QInputDialog.TextInput) 
        dlg.setLabelText("Project Name:")  
        dlg.setWindowTitle("Enter Project Name")                      
        dlg.resize(500,1500)                             
        ok_pressed = dlg.exec_()                                
        text = dlg.textValue()   
        
        print ("HEY", ok_pressed)
        
#        text, ok_pressed = QInputDialog.getText(self, "Enter text","Project Name:", QLineEdit.Normal, "")
        if (ok_pressed == 1) and text != '':
            return text
        else:
            return -1
    
    def find_button_by_text(self, text):
         """
         Returns the QPushButton instance
         :param text: the button text
         """
         return (self.manager.existing_project_labels[text])

    def show_appropriate_window(self):
        """
        This function shows the appropriate window for whatever project.
        So if a user creates 10 projects, the 5th button shows the 5th window.
        
        The project manager contains all the existing projects as an object.
            It contains an array called projects which has pair-wise tuples of:
                    (project, window)
        
        Returns: Void
        """
        
        
        # Identify the label first, which was clicked. And show the appropriate project.
        
        desired_button = self.find_button_by_text(self.sender().text())
        self.manager.projects[desired_button][1].show()
        
        print (self.sender().text())
        
        
    
    def new_project_window(self):                
        """
        Event that a new project button is clicked. 
        Create a new project, update relevant stuff.
                            
        Returns: Void.
        """
        button_name = self.get_text()
        if (button_name == -1): return
                   

        # Make a brand new project template.
        new_project = Project()

        # Make a brand new window.
        new_window = gui_h.New_Project_Window(new_project)
        
        # show the window to confirm project-creation just once.
        new_window.show()

        # Add the appropriate values to the project manager class object.
        
        # Finally, increment the total tally of projects existing.
        self.counter += 1
        
        # Make a brand new button.
        existing_project_btn = QPushButton("{} + {}".format(button_name, self.counter), self)        
        self.manager.add(new_project, new_window, existing_project_btn)

        new_posx = self.manager.projects[existing_project_btn][2]
        new_posy = self.manager.projects[existing_project_btn][3]
        existing_project_btn.move(new_posx, new_posy)
        
        # This is broken, ? Each connect is being overwritten.
        
        # Add the button on the main menu, with an unique identifier as pair-wise tuples to the project manager.
        self.manager.add_label(existing_project_btn, existing_project_btn.text())
        
        existing_project_btn.clicked.connect(self.show_appropriate_window) 
        existing_project_btn.show()
        
        
        # Just debugging here.
        self.manager.show_all()
        

    
    def add_new_project_button(self):
        """
        Adds the "new project" button on to the screen
        Returns
        -------
        None.
        """
        
        new_project_btn = QPushButton("New Project", self)
        new_project_btn.resize(250,150)
        new_project_btn.clicked.connect(self.new_project_window) 
        
    
        new_project_btn.move(200, 200)
        
    def debug(self):
        print("Click me harder!")