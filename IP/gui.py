# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:10:34 2021

@author: garvi
"""

import gui_helper as gui_h
import saving_utility as su
from my_Error import my_Error

from project import Project

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QDesktopWidget, \
                            QInputDialog, QCheckBox, QShortcut, QTextEdit, QMessageBox
from PyQt5.QtGui import QKeySequence, QDrag
from PyQt5.QtCore import QSettings, Qt, QMimeData

import pickle

class Button(QPushButton):
    
    def __init__(self, title, parent):
        super().__init__(title, parent)

    def mouseMoveEvent(self, e):
        '''
        Enable drag for buttons.
        '''
        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)

class Main_Screen(su.QMainWindow):
    # The template for the main-screen that is showed when the user boots up the software.
    def __init__(self, project_manager, parent = None):
        super(Main_Screen, self).__init__(project_manager, parent)
        self.title = "TESTING-MODEL-2d from 0a (CTRL+Q to quit)"
        
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

        self.delete_widgets = []

        self.setAcceptDrops(True)

        self.existing_offsety = 0
        arr = self.restored_array
        if (arr != []):
            # There are values here, thus the user is starting this for the second time. 
            print(arr)
            #self.counter += 1
            self.reinit_UI(arr)
            
        else:
            # Initilaize a UI to use
            self.init_UI()
            
        # By default, the active project title is the first project itself.
        if (arr != []):
            self.active_project_title = self.manager.projects[list(self.manager.projects.keys())[0]][0].name
        else:
            self.active_project_title = ""
            
        
        # ----------------------- Debugging ------------------------------        
        # TODO
        # Widgets to delte subtasks.
        self.testing = 0
                
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


    def sort(self, sub_li):
        '''
        Credit: https://stackoverflow.com/questions/17555218/python-how-to-sort-a-list-of-lists-by-the-fourth-element-in-each-list/17555237
        This snippet is not mine.
        '''
        return sorted(sub_li, key = lambda x: int(x[3][len("button__"):]))
    
    def reinit_UI(self, dynamic_widgets):
        '''
        Description:
            Reinit the window based on dynamically created widgets.
        '''
        
        # This loads the pickled subprojects. That is, tasks accompanying each projects.
            # {button_text = (project, posx, posy)}
        try:
            reloaded_dict = pickle.load(open("subproj.dat", "rb"))
        except:
            su.closeEvent()
            
        print (reloaded_dict)
        
        
        assert len(reloaded_dict) == len(dynamic_widgets), "\n\nYour data is corrupted, you modified the dat file or HKEY directory. Delete your entire HKEY and subproj.data to start again, this time dont fuck around."
                        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.quitSc = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quitSc.activated.connect(QApplication.instance().quit)

    
        self.center_object(self)
        self.add_new_project_button()
        
        # Restore the dynamically created widgets by the user.
        
        self.reinitialized_button_list = []
        
        # sometimes the REGEDIT takes in values that are clonky.
            # If wrong order, all the stuff is fucked.
        dynamic_widgets = self.sort(dynamic_widgets)
        for widget in dynamic_widgets:
            button_name = widget[3]
            button_id = (button_name[len("button__"):])
            
            if (button_id == "-1"): continue
            # (text, geometry, size, name of the widget in HKEY directory)
            new_widget = Button(widget[0], self)
            
            size = widget[1]
            new_widget.resize(size.width(), size.height())
           # new_widget.setCheckable(True)     
            
            new_widget.move(size.x(), size.y())
            new_widget.adjustSize()
            
            self.reinitialized_button_list.append(new_widget)
        
            # Some random delta. This helps when you re-init shit.
            #self.existing_offsety += 35
            self.counter += 1

        # The manager class holds (project, window, posx, posy)         
        # the project dict in project_manager has the follwoing container:
            # {button = (project, window, self.positionx, self.positiony)}

        # The exisiting label dict has the following container:
            # {button: button_text}
        
        i = 0
        for key in reloaded_dict.keys():
            # The key contain the text.
            button_text = key
            try:
                self.manager.add_label(self.reinitialized_button_list[i], button_text)
            except:
                print ("one label was not added mate")
                break
                        
            # Make the window object so the appropriate segue happens upon clicking or better put, toggling.
            generic_window = gui_h.New_Project_Window(reloaded_dict[key][0])      
            generic_window_sub_str = generic_window.display_data()

            self.show_new_sub_project(generic_window_sub_str)
            self.isLabel = True
            
            print ("\n\n")
            self.reinitialized_button_list[i].clicked.connect(self.show_appropriate_window)
            
            self.manager.add(reloaded_dict[key][0], generic_window, self.reinitialized_button_list[i])
            i += 1
            pass


        self.reload_delete_keys(self.manager.projects[list(self.manager.projects.keys())[0]][0])
        self.show()        
        self.show_new_sub_project(self.manager.projects[list(self.manager.projects.keys())[0]][0].display_data())


    def reload_delete_keys(self, some_project):
        '''
        Reload all the delete_keys for whichever project being displayed.
        '''
        if (self.delete_widgets != []):
            print (self.delete_widgets)
            # There is already a bunch of deletes on screen, delete them.
            for widget in self.delete_widgets:
                widget.clicked.connect(self.doNothing)
                widget.deleteLater()
            
            self.delete_widgets = []
                
        posy = 0
        for i in range(some_project.num_sub_tasks):
            testing = QPushButton("Delete {}".format(i+1), self)
            testing.resize(20,20)
            testing.move(830,posy)
            testing.adjustSize()
            testing.show()
            
            self.delete_widgets.append(testing)
            posy += 20
            
            # Connect the newly formed fresh keys from the oven.
            self.connect_delete_keys()
            
        self.active_project = some_project

    def doNothing(self):
        return
    
    
    def delete_project(self):
        '''
        Delete the active project on screen.
        Onclick for "Delete This Project" QPushButton
        '''
        
        # When a project is removed, simply update project manager, that should be enough.
            # Also, make the button vanish.
        
        project_dict = self.manager.projects
        idx = 0
        try:
            idx, button_to_delete = self.find_button_by_project(self.active_project)
            del project_dict[button_to_delete]
            button_to_delete.deleteLater()
            
            if (list(project_dict.keys()) != []):
                new_project_btn = list(project_dict.keys())[0]
                new_project_btn.click()

        except:
            my_Error.add_a_project(self)
            return
        
        
        if (self.restored_array == []):
            # Done. First time loading, no need to update regedit or whatever.
            return
            
        
        # The deletion is successful, update the restored array to make sure this button is not saved.
            # If it's removed it will trigger assertion fail.
        
        if (project_dict == {}):
            # THe user deleted the last project that happened to NOT be the first one.
            # in this scenario, 
            setting_to_delete = "User Settings/" + str(self.restored_array[0][3])
            del self.restored_array[0]
            self.settings.remove(setting_to_delete)
            return
        
        
        setting_to_delete = "User Settings/" + str(self.restored_array[idx][3])
        del self.restored_array[idx]
        
        
        #update regedit
        self.settings.remove(setting_to_delete)

        print(self.active_project.name)
    
    def connect_delete_keys(self):
        '''
        See: reload_Delete_keys, pretty self explanatory.
        '''
        for keys in self.delete_widgets:
            keys.clicked.connect(self.delete_sub_project)
            #value_to_delete = int(self.delete_widgets[keys][len("Delete "):]) - 1
            #print(value_to_delete)
        
    def delete_sub_project(self):
        '''
        See: connect_delete_keys.
        '''
        if (isinstance(self.sender(), QPushButton) == False): return
        
        value_to_delete = int((self.sender().text())[len("Delete "):]) - 1
        
        # Value to delete holds the subtask for whichever project that needs deletion.
        print(value_to_delete)
        
        # self.active_project holds the current project on screen.
            # The way the buttons are created it programatically creates a CLICK event.
            # It is almost guaranteed with 69% certainty that active project is indeed active project.
            # Still, put a warning on screen.
        print(self.active_project.num_sub_tasks)
        
        
        # Value to delete holds the sub task that needs to go.
        
        del self.active_project.sub_tasks[value_to_delete]
        self.active_project.num_sub_tasks = len(self.active_project.sub_tasks)
        
        
        # Reload the delete keys.
        self.reload_delete_keys(self.active_project)
        
        
        # click the button programatically to real-time update deleted subprojects.
        _, btn = self.find_button_by_project(self.active_project)
        btn.click()
        
        
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
    
    def find_button_by_project(self, project):
        count = 0
        for key, value in self.manager.projects.items():
            if (value[0] == project):
                return count, key
            count += 1
            
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
            # {button = (project, window, self.positionx, self.positiony)}
        active_project = self.manager.projects[desired_button][0]
        string = active_project.display_data()
        
        self.active_project_title = active_project.name
        self.active_button = desired_button

        # ----------------------- Debugging ------------------------------
                                   # TODO        
        if (self.debug_check.isChecked()):
                # {button = (project, window, self.positionx, self.positiony)}
            desired_window = self.manager.projects[desired_button][1]
            desired_window.update_project(active_project)
            desired_window.display_data()
            desired_window.show()
        # ----------------------- Debugging ------------------------------
        else:
            self.show_new_sub_project(string, active_project)
            print (self.sender().text())
            
    def find_project_by_name(self, title):
        '''
        Find project object by its title from the project manager class and associated dictionaries.
        The projects dict in project_manager contains: {button: (projects, window, x, y)}
        '''
        for key in self.manager.projects.keys():
            if (self.manager.projects[key][0].name == title):
                return self.manager.projects[key][0]
    
    def get_sub_project_counter(self, active_project):
        '''
        A function to retrieve existing sub projects, if there are 4, return that.
        params:
            active_project: the project being displayed on the screen.
        '''
        
        if (active_project == None):
            my_Error.add_a_project(self)
            return
            
        return active_project.num_sub_tasks
    
    def add_sub_project_to_projects(self):
        '''
        First, check which project class is active.
        Second, add a sub-project to it.
        '''
        
        active_project = self.find_project_by_name(self.active_project_title)
        # get the existing number of sub projects.
        self.sub_project_counter = self.get_sub_project_counter(active_project)
                
        try:
            active_project.add_sub_project(self.sub_project_counter)
            self.sub_project_counter += 1            

            # The project on screen has changed, reload delete keys for this project.
            self.reload_delete_keys(active_project)
                    
            self.show_new_sub_project(active_project.display_data())
        except:
            my_Error.add_a_project(self)
    
    def show_new_sub_project(self, string, project=None):
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
        self.string_label.move(550,0)
        self.string_label.show()
        self.string_label.adjustSize()
        self.isLabel = True 

        if (project != None):
            self.reload_delete_keys(project)
    
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
                
        # Set the names based on user input
        new_project.name = button_name
        new_project.sub_tasks[0].project_name = button_name
        
        # Make a brand new window.
        new_window = gui_h.New_Project_Window(new_project)
        new_project_sub_string = new_project.display_data()

        self.show_new_sub_project(new_project_sub_string)
        self.isLabel = True

        # Finally, increment the total tally of projects existing.
        self.counter += 1
        
        # Make a brand new button.
        existing_project_btn = Button("{} + {}".format(button_name, self.counter), self)        
        self.manager.add(new_project, new_window, existing_project_btn)
        
        new_posx = self.manager.projects[existing_project_btn][2]
        new_posy = self.manager.projects[existing_project_btn][3] + self.existing_offsety
        
        existing_project_btn.move(new_posx, new_posy)
                
        # Add the button on the main menu, with an unique identifier as pair-wise tuples to the project manager.
        self.manager.add_label(existing_project_btn, existing_project_btn.text())
        
        # Here the onclick event takes place to link each project with its subtasks.
        existing_project_btn.clicked.connect(self.show_appropriate_window)
        existing_project_btn.adjustSize()
        existing_project_btn.show()
        
        existing_project_btn.click()
        
        if (self.active_project_title == ""):
            self.active_project_title = new_project.name
                
        # Just debugging here.
        self.manager.show_all()
        
        # The project on screen has changed, reload delete keys.
        self.reload_delete_keys(new_project)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        #self.button.move(position)
        
        # Find the button screen that is active, and move it.
        try:
            self.active_button.move(position)
        except:
            my_Error.click_button_first(self)
        
        e.setDropAction(Qt.MoveAction)
        e.accept()

    def add_new_project_button(self):
        '''
        Adds the "new project" button on to the screen
        Adds the "new sub project" button on to the screen
        
        This happens both in reinit or init.
        '''   
        new_project_btn = QPushButton("New Project", self)
        new_project_btn.resize(250,150)
        new_project_btn.move(200, 200)
        new_project_btn.clicked.connect(self.new_project_window) 
        
        new_sub_project_btn = QPushButton("New Sub-Project", self)
        new_sub_project_btn.resize(100,20)
        new_sub_project_btn.move(140,0)
        new_sub_project_btn.clicked.connect(self.add_sub_project_to_projects)


        new_sub_project_btn = QPushButton("Delete This Project", self)
        new_sub_project_btn.resize(100,20)
        new_sub_project_btn.move(140,20)
        new_sub_project_btn.clicked.connect(self.delete_project)
        
        
        information_label = QLabel("Left click on a project button to move it!", self)
        information_label.resize(100,20)
        information_label.move(250,370)
        information_label.adjustSize()

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