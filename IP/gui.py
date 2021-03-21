# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:10:34 2021

@author: garvi
"""

import sys
import gui_helper as gui_h

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDesktopWidget, QInputDialog, QCheckBox

from project import Project

class Main_Screen(QWidget):
    # The template for the main-screen that is showed when the user boots up the software.
    def __init__(self, project_manager):
        super().__init__()
        self.title = "TESTING-MODEL-2a (First version was 0a)"
        
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        
        # Initilaize a UI to use
        self.init_UI()
        
        # Initiliaze a Project Manager Class Object.
        self.manager = project_manager
        
        # A counter to track the projects, it helps to show which window to display.
        self.counter = -1
                
        # To show only one relevant sub-project index for each project at one time.
        self.isLabel = False

        
    def center_object(self, desired_object):
        """
        Params:
            desired_obj - object to center
            
        Description:
            Center object wrt desktop not the window.
        """
                

        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()

        qtRectangle.moveCenter(centerPoint)
        desired_object.move(qtRectangle.topLeft())
        
    def init_UI(self):
        '''
        Description:
            Sets window title,
            Sets geometry,
            Centers the screen wrt desktop,
            Shows the screen.
        '''
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center_object(self)
        self.add_new_project_button()
        self.show()
        
        
    def get_text(self):
        '''
        Description:
            The dialog when the "New project" button is clicked.
            Returns -1 if the user doesn't input anything or just closes the dialog.
        '''
        dlg =  QInputDialog(self)                 
        dlg.setInputMode( QInputDialog.TextInput) 
        dlg.setLabelText("Project Name:")  
        dlg.setWindowTitle("Enter Project Name")                      
        dlg.resize(500,1500)                             
        ok_pressed = dlg.exec_()                                
        text = dlg.textValue()   
        
        if (ok_pressed == 1) and text != '': return text
        else: return -1
    
    def find_button_by_text(self, text):
         '''
         Params:
             text - string that identifies each button.
             self.manager - project manager objetc
         
        Returns:
            The button that is found with each text, so that the subproject data is appropriately shown.
         '''
         return (self.manager.existing_project_labels[text])

    def show_appropriate_window(self):
        '''
        Once the button is found, show the appropriate window using project mangers dictionaries.
        See: find_button_by_text()
        '''                
        desired_button = self.find_button_by_text(self.sender().text())
        string = self.manager.projects[desired_button][0].sub_tasks[0].display_data()

        # ----------------------- Debugging ------------------------------
                                   # TODO        
        if (self.debug_check.isChecked()):
            self.manager.projects[desired_button][1].show()   
        # ----------------------- Debugging ------------------------------
        else:
            self.show_new_sub_project(string)
            print (self.sender().text())
            
    
    def show_new_sub_project(self, string):
        '''
        A function to clear the subproject label on screen incase a new project is clicked.
        I.e, 
                Project a has x subtask. Project b has y subtask.
                When a is clicked show x, when b is clicked, clear x and show y.
        
        params:
            string - contains the strings for each subprojct/task.
        
        returns:
            displays data on same window
        '''
        if(self.isLabel):
            self.string_label.clear()
            self.isLabel = False

        self.string_label = QLabel(string, self)
        self.string_label.move(250,0)
        self.string_label.show()
        self.isLabel = True            

    def new_project_window(self):                
        '''
        Create a new project window when the button is clicked. Think of this as @onclickevent.
        Show it,
        Update the project - manager.
        Use Project, Subproject class to show default data for a NEW project.
        '''
        button_name = self.get_text()
        if (button_name == -1): return

        # Make a brand new project template.
        new_project = Project()
        # Make a brand new window.
        new_window = gui_h.New_Project_Window(new_project)      
        
            
        new_project_sub_string = new_window.display_data()

        # ----------------------- Debugging ------------------------------
                                   # TODO
        if (self.debug_check.isChecked()):
            new_window.show()
            new_window.display_data()
        # ----------------------- Debugging ------------------------------
        
        self.show_new_sub_project(new_project_sub_string)
        self.isLabel = True

        # Finally, increment the total tally of projects existing.
        self.counter += 1
        
        # Make a brand new button.
        existing_project_btn = QPushButton("{} + {}".format(button_name, self.counter), self)        
        self.manager.add(new_project, new_window, existing_project_btn)

        new_posx = self.manager.projects[existing_project_btn][2]
        new_posy = self.manager.projects[existing_project_btn][3]
        existing_project_btn.move(new_posx, new_posy)
                
        # Add the button on the main menu, with an unique identifier as pair-wise tuples to the project manager.
        self.manager.add_label(existing_project_btn, existing_project_btn.text())
        
        # Here the onclick event takes place to link each project with its subtasks.
        existing_project_btn.clicked.connect(self.show_appropriate_window) 
        existing_project_btn.show()
                
        # Just debugging here.
        self.manager.show_all()
    
    def add_new_project_button(self):
        '''
        Adds the "new project" button on to the screen
        '''        
        new_project_btn = QPushButton("New Project", self)
        new_project_btn.resize(250,150)
        new_project_btn.clicked.connect(self.new_project_window) 
        new_project_btn.setCheckable(True) 

        new_project_btn.move(200, 200)
        
        
        # This adds a checkbox on the screen it will be removed later its just handy for debugging.
        # ----------------------- Debugging ------------------------------        
        # TODO
        self.debug_check = QCheckBox("New Window? [Debug]", self)
        self.debug_check.move(105,0)
        self.debug_check.show()
        # ----------------------- Debugging ------------------------------
        
    def debug(self):
        print("Click me harder!")