# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:10:34 2021

@author: garvi
"""

import gui_helper as gui_h
import testing_random_snippets as ta
from project import Project


from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QDesktopWidget, QInputDialog, QCheckBox, QShortcut
from PyQt5.QtGui import QKeySequence
import pickle


class Main_Screen(ta.QMainWindow):
    # The template for the main-screen that is showed when the user boots up the software.
    def __init__(self, project_manager, parent = None):
        super(Main_Screen, self).__init__(project_manager, parent)
        self.title = "TESTING-MODEL-2d (First version was 0a \tCTRL+Q to quit)"
        
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        
        #self.init_UI()
        
        # Initiliaze a Project Manager Class Object.
        self.manager = project_manager
        
        # A counter to track the projects, it helps to show which window to display.
        self.counter = -1
                
        # To show only one relevant sub-project index for each project at one time.
        self.isLabel = False

        self.existing_offsety = 0
        arr = self.restored_array
        if (arr != []):
            # There are values here, thus the user is starting this for the second time. 
            print(arr)
            self.counter += 1
            self.reinit_UI(arr)
            
        else:
            # Initilaize a UI to use
            self.init_UI()
        
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
 
        self.quitSc = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quitSc.activated.connect(QApplication.instance().quit)

    
        self.center_object(self)
        self.add_new_project_button()
        self.show()

    def reinit_UI(self, dynamic_widgets):
        '''
        Description:
            Reinit the window based on dynamically created widgets.
        '''
        
        # This loads the pickled subprojects. That is, tasks accompanying each projects.
        reloaded_dict = pickle.load(open("subproj.dat", "rb"))
        
        print (reloaded_dict)
#        print (reloaded_dict['button__1'][0].sub_tasks[0].display_data())
        
        # The manager class holds (project, window, posx, posy) 
        # The reloaded dict for pickle reasons contains all but the second value. 
        
        # The button as a key is missing, however, the find_button_by_text implies that's not hard.
        # Reinitiliaze the manager object and it should all work seemlessly. (is that how u spell it?)
        
        # the project dict in project_manager has the follwoing container:
            # {button = (project, window, self.positionx, self.positiony)}

        # The exisiting label dict has the following container:
            # {button: button_text}
        
        new_project_dict = {}
        new_existing_label_dict = {}
        
        for key in reloaded_dict.keys():
            # The key contain the text.
            button = self.find_button_by_text(reloaded_dict[key])
            button_text = reloaded_dict[key]
            
            # Make the window object so the appropriate segue happens upon clicking or better put, toggling.
            
            
            # Second dict re-initialized, done.
            new_existing_label_dict[button] = button_text
            pass
        
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.quitSc = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quitSc.activated.connect(QApplication.instance().quit)

    
        self.center_object(self)
        self.add_new_project_button()
        
        # Restore the dynamically created widgets by the user.
        for widget in dynamic_widgets:
            button_name = widget[3]
            button_id = (button_name[len("button__"):])
            if (button_id == "-1"): continue
            # (text, geometry, size, name of the widget in HKEY directory)
            new_widget = QPushButton(widget[0], self)
            
            size = widget[1]
            new_widget.resize(size.width(), size.height())
            new_widget.setCheckable(True)     
            
            new_widget.move(size.x(), size.y())
            new_widget.adjustSize()
            
            # Some random delta. This helps when you re-init shit.
            self.existing_offsety += 35
            self.counter += 1
        
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
        self.string_label.adjustSize()
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
        new_posy = self.manager.projects[existing_project_btn][3] + self.existing_offsety
        
        # TODO: Fix this based on existing labels in the dictionary.
        existing_project_btn.move(new_posx, new_posy)
                
        # Add the button on the main menu, with an unique identifier as pair-wise tuples to the project manager.
        self.manager.add_label(existing_project_btn, existing_project_btn.text())
        
        # Here the onclick event takes place to link each project with its subtasks.
        existing_project_btn.clicked.connect(self.show_appropriate_window)
        existing_project_btn.adjustSize()
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
        self.debug_check.move(250,350)
        self.debug_check.adjustSize()
        self.debug_check.show()
        # ----------------------- Debugging ------------------------------
        
    def debug(self):
        print("Click me harder!")