# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:10:34 2021

@author: garvi
"""

import gui_helper as gui_h
import saving_utility as su

from my_Error import my_Error
from Dialogues import Dialog
from project import Project

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QDesktopWidget, \
                            QInputDialog, QCheckBox, QShortcut, QWidget, QGridLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QKeySequence, QDrag, QFont
from PyQt5.QtCore import Qt, QMimeData

import pickle

IP_VERSION = "IP Version 2f"

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
    def __init__(self, project_manager, parent = None):
        super(Main_Screen, self).__init__(project_manager, parent)
        self.title = "{} (CTRL+Q to quit)".format(IP_VERSION)


        self.widget = QWidget(self)
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
    
    
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.existing_offsety = 25
                
        # Initiliaze a Project Manager Class Object.
        self.manager = project_manager        
    
        # A counter to track the projects.
        self.counter = -1
    
        # Islabel on screen for project?
        self.isLabel = False

        # Delete each project widgets, dynamically made.
        self.delete_widgets = []
        
        # Each subproject button widgets.
        self.subproject_widgets = []
        self.setAcceptDrops(True)

        # Taken from saving_utility.py Check superclass
        arr = self.restored_array
        
        if (arr != []):
            # Re-initialize all data.
            self.reinit_UI(arr)            
        else:
            self.init_UI()
            
        if (arr != []):
            self.active_project_title = self.manager.projects[list(self.manager.projects.keys())[0]][0].name
        else:
            self.active_project_title = ""
            self.active_project = None
            
        
        # Active SP on the screen.
        self.active_sp = None
        self.test_label = None
        
        

                            
    def center_object(self, desired_object):
        """
        Centers any object on to the desktop.
        desired_object is the object of choice
        """
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()

        qtRectangle.moveCenter(centerPoint)
        desired_object.move(qtRectangle.topLeft())
        
    def init_UI(self, show = 1):
        '''
        Description:
            Sets window title, geometry, Centers the screen wrt desktop, Shows the screen.
        '''
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center_object(self)

        self.add_new_project_button()

        self.quitSc = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quitSc.activated.connect(QApplication.instance().quit)

        # To stop deduplicating code, reinit uses the same code block above.
        if (show == 1):
            self.show()

    def sort(self, sub_li):
        '''
        Credit: https://stackoverflow.com/questions/17555218/python-how-to-sort-a-list-of-lists-by-the-fourth-element-in-each-list/17555237
        This snippet is not mine.
        
        I've developed this habit through a class I took in Spring '21. 
        '''
        return sorted(sub_li, key = lambda x: int(x[3][len("button__"):]))
    
    def reinit_UI(self, dynamic_widgets):
        '''
        Description:
            Reinit the window based on dynamically created widgets.
        '''        
        try:
            reloaded_dict = pickle.load(open("subproj.dat", "rb"))
        except:
            su.closeEvent()
        
        assert len(reloaded_dict) == len(dynamic_widgets), "\n\nYour data is corrupted, you modified the dat file or HKEY directory. Delete your entire HKEY to start again."
        
        # Do what init UI does on first run minus the show, until data processing is done.
        self.init_UI(show = 0)
        self.reinitialized_button_list = []
                # sometimes the REGEDIT takes in values that are clonky. Fix with sort.
        dynamic_widgets = self.sort(dynamic_widgets)

        for widget in dynamic_widgets:
            # format: (text, geometry, size, name of the widget in HKEY directory)
                    # This format is how saving_utility.py saves it.

            button_name = widget[3]
            button_id = (button_name[len("button__"):])
            
            if (button_id == "-1"): continue
            new_widget = Button(widget[0], self)
            
            size = widget[1]
            new_widget.resize(size.width(), size.height())
            
            new_widget.move(size.x(), size.y())
            #new_widget.adjustSize()
            
            self.reinitialized_button_list.append(new_widget)
            # Add to counter (project tracker)
            self.counter += 1

        # The manager class holds (project, window, posx, posy)         
            # the project dict in project_manager has the follwoing container:
                    # {button = (project, window, self.positionx, self.positiony)}
            # The exisiting label dict has the following container:
                    # {button: button_text}
        
        widget_idx = 0
        for key in reloaded_dict.keys():
            button_text = key
            try:
                self.manager.add_label(self.reinitialized_button_list[widget_idx], button_text)
            except:
                print ("Label addition failed")
                break
            
            # Make the window object so the appropriate segue happens upon clicking or better put, toggling.
            generic_window = gui_h.New_Project_Window(reloaded_dict[key][0])      
            generic_window_sub_str = generic_window.display_data()
            
            self.show_new_sub_project_clutter(generic_window_sub_str)
            self.isLabel = True
            
            print ("\n\n")
            self.reinitialized_button_list[widget_idx].clicked.connect(self.show_appropriate_window)
            
            self.manager.add(reloaded_dict[key][0], generic_window, self.reinitialized_button_list[widget_idx])
            widget_idx += 1
            pass

        # Reload delete keys, show the window, show-new-sub-project button.
        self.reload_delete_keys(self.manager.projects[list(self.manager.projects.keys())[0]][0])
        self.show()
        
        # This scary line just shows the first projects subproject instances on a REINIT.
            # lol I saw a video called "Trust by Design" on TedEx where the airbnb guy talked about how ...
            # ... People trust his app without fear of getting sodomized.
        
        self.show_sub_project_names(self.manager.projects[list(self.manager.projects.keys())[0]][0].get_data())
#        self.show_new_sub_project_clutter(self.manager.projects[list(self.manager.projects.keys())[0]][0].display_data())

    def reload_delete_keys(self, some_project):
        '''
        Reload all the delete_keys for whichever project being displayed.
        
        Project Y may have 3 subtasks and X has 4...
        Delete 3 and 4 wrt which is being showed on-screen.
        '''
        if (self.delete_widgets != []):
            print (self.delete_widgets)
            # There is already a bunch of deletes on screen, delete them.
            for widget in self.delete_widgets:
                widget.clicked.connect(self.doNothing)
                widget.deleteLater()
            
            self.delete_widgets = []
                    
        
        #        self.debug_check.move(400,0)    
        #   The delete keys go to the right of the check mark. so this is useful if someone fiddles with this.
        posx = 540
        #        new_sub_project_btn.resize(100,20)
        for i in range(some_project.num_sub_tasks):
            new_del_btn = QPushButton("Delete {}".format(i+1), self)
            new_del_btn.move(posx,0)
            new_del_btn.resize(85,20)
            new_del_btn.show()
            
            self.delete_widgets.append(new_del_btn)
            posx += 85
            
            # Connect the newly formed fresh keys from the oven.
            self.connect_delete_keys()
        
        # Change self.active_project important line here
        self.active_project = some_project
    
    def find_sub_task_by_index(self, project, index_to_find):
        '''
        Given raw index, find that index in the project subtask array. It may vary.
        Find first such occurance as indexes are all unique.
        '''
        for index, subprojects in enumerate(project.sub_tasks):
            if (subprojects.idx == index_to_find):
                return index

    def edit_project(self):  
        '''
        Edits the project based on the Dialogues.py file.
        Show the dialog -> Get data -> Change the project manager.
        Saving drives the rest.
        '''
        try:
            dialog = Dialog(self.active_project)
            ok_pressed = dialog.exec_()
            
            if (ok_pressed == 1):
                data = dialog.extract_data()    
            else:
                return
            
            # data must be in the form [projectname, subtaskindex, subtaskname, subtaskmemebers, subtask ETA]
            if (data[0] != ""): self.active_project.name = data[0]
            

# ----------------------------------------------------------------------------------------
# TODO
            # change the name of the button.
      #      _, self.active_button = self.find_button_by_project(self.active_project)
       #     unique_id = self.active_button.text()[len(self.active_button.text()) - 4:]
        #    new_button_name = data[0] + unique_id
         #   self.active_button.setText(new_button_name)
            
            # Project manager must be changed as well to ripple out those changes.
            
            # Further, the button holding this value in the local cache should ALSO be changed.
            
# ----------------------------------------------------------------------------------------
            
            index_of_subtask = self.find_sub_task_by_index(self.active_project, int(data[1]))

            if(data[2] != ""): self.active_project.sub_tasks[index_of_subtask].name = data[2]
            
            _, project_btn = self.find_button_by_project(self.active_project)
            project_btn.click()
        
        
        except:
            my_Error.add_a_project(self)       

        
    def doNothing(self):
        '''
        Does nothing this is actually very useful code I'm not joking.
        '''
        return
    
    def delete_project(self):
        '''
        Delete the active project on screen.
        Onclick for "Delete This Project" QPushButton
        '''
        confirmation_status = my_Error.confirm_deletion(self, self.active_project.name, self.active_project.num_sub_tasks)
        
        # 1 is okay, -1 is cancel.
        if (confirmation_status == -1): return
        
        project_dict = self.manager.projects
        idx = 0
        try:
            idx, button_to_delete = self.find_button_by_project(self.active_project)
            del project_dict[button_to_delete]
            button_to_delete.deleteLater()
            
            if (list(project_dict.keys()) != []):
                new_project_btn = list(project_dict.keys())[0]
                new_project_btn.click()
            
            else:
                # You deleted the last project, flush all the UI stuff.
                self.flush_delete_sp_buttons()
            

        except:
            my_Error.add_a_project(self)
            return
        
        if (self.restored_array == []):
            # Done. First time loading, no need to update regedit or whatever.
            # OR the user has deleted the first entry or project now theres nothing left.
            if (project_dict == {}):
                self.flush_delete_sp_buttons()

            return            
        
        # The deletion is successful, update the restored array to make sure this button is not saved.
            # If it's removed it will trigger assertion fail.
        
        if (project_dict == {}):
            # THe user deleted the last project that happened to NOT be the first one.
            setting_to_delete = "User Settings/" + str(self.restored_array[0][3])
            del self.restored_array[0]
            self.settings.remove(setting_to_delete)
            return        
        
        try:
            # The only time this try block fails is if you delete a project that you made after a reinit.
            # Technically, that project will only save AFTER the program exits, with my saving_utility.py.
            
            # In that case, it doesn't exist on the regedit YET.
            setting_to_delete = "User Settings/" + str(self.restored_array[idx][3])
            del self.restored_array[idx]

            #update regedit
            self.settings.remove(setting_to_delete)
            
        except:
            pass
        
        # sometimes, the user deletes the last project, dont leave the lingering subtasks on screen
        print(self.active_project.name)
    
    def connect_delete_keys(self):
        '''
        See: reload_Delete_keys, pretty self explanatory.
        '''
        for keys in self.delete_widgets:
            keys.clicked.connect(self.delete_sub_project)
        
    def delete_sub_project(self):
        '''
        See: connect_delete_keys.
        '''
        if (isinstance(self.sender(), QPushButton) == False): return
        
        value_to_delete = int((self.sender().text())[len("Delete "):]) - 1        
        # Value to delete holds the subtask for whichever project that needs deletion.
        print(value_to_delete)
        print(self.active_project.num_sub_tasks)
                
        try:
            del self.active_project.sub_tasks[value_to_delete]
        except:
            return
        self.active_project.num_sub_tasks = len(self.active_project.sub_tasks)
        
        # Reload the delete keys.
        self.reload_delete_keys(self.active_project)
                
        # click the button programatically to real-time update deleted subprojects.
        _, btn = self.find_button_by_project(self.active_project)
        btn.click()        
        
    def get_text(self):
        '''
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
        '''
        Navigate project manager to find button by project object.
        '''
        count = 0
        for key, value in self.manager.projects.items():
            if (value[0] == project):
                return count, key
            count += 1

    def find_project_by_button(self, button):
        '''
        Navigate project manager to find project by button object.
        '''
                # Projects:             A Dictionary that contains {button: (projects, window, x, y)}
        
        for key, value in self.manager.projects.items():
            if (key == button):
                return value[0]
            
    def find_button_by_text(self, text):
         '''
         Navigate project manager to find button by project title text.
         '''
         return (self.manager.existing_project_labels[text])

    def show_appropriate_window(self):
        '''
        Show the appropriate window using project mangers dictionaries.
        See: find_button_by_text()
        '''                
        desired_button = self.find_button_by_text(self.sender().text())
            # {button = (project, window, self.positionx, self.positiony)}
        active_project = self.manager.projects[desired_button][0]
        
        self.active_project_title = active_project.name
        self.active_button = desired_button
        
        self.active_project = active_project

        # ----------------------- Debugging ------------------------------
        if (self.debug_check.isChecked()):
                # {button = (project, window, self.positionx, self.positiony)}
            desired_window = self.manager.projects[desired_button][1]
            desired_window.update_project(active_project)
            desired_window.display_data()
            desired_window.show()
        # ----------------------- Debugging ------------------------------
        else:
#            self.show_new_sub_project(string, active_project)
            
            self.show_sub_project_names(active_project.get_data())
            print (self.sender().text())
            
    def find_project_by_name(self, title):
        '''
        Navigate project manager to find project by title of project.
        The projects dict in project_manager contains: {button: (projects, window, x, y)}
        '''
        for key in self.manager.projects.keys():
            if (self.manager.projects[key][0].name == title):
                return self.manager.projects[key][0]
    
    def get_sub_project_counter(self, active_project):
        '''
        I dont know what this does. My comment was a funny joke which is pretty unfunny now.
        
        Finds the number of tasks for whichever active project on screen.
        If  there is no active project, return nothing.
        '''
        if (active_project == None):
            my_Error.add_a_project(self)
            return -1
            
        return active_project.num_sub_tasks
    
    def add_sub_project_to_projects(self):
        '''
        -> Check which project class is active.
        -> Add a sub-project to it.
        '''
        active_project = self.find_project_by_name(self.active_project_title)
        # get the existing number of sub projects.
        self.sub_project_counter = self.get_sub_project_counter(active_project)
        
        # Save CPU
        if (self.sub_project_counter == -1): return
        
        try:
            active_project.add_sub_project(self.sub_project_counter)
            self.sub_project_counter += 1
            # The project on screen has changed, reload delete keys for this project.
            self.reload_delete_keys(active_project)    
            self.show_sub_project_names(active_project.get_data())
        except:
            my_Error.add_a_project(self)
            return
                
    #TODO - 0
        # Once team members are added properly, Just show that data here once the button is clicked.
    def connect_sp_keys(self):
        '''
        A function to connect the SP keys once they're made.
        Each project tab has subprojects, this function links them.
        
        Think as @onclick for subproject btns.
        
        Note to self: Dont try returning if there are no SP's. If there are no SPs there are no keys.
                        lol. 3AM coding is fun isnt it
        '''
        sp_details = self.sender().text()
        sp_index = ""
        for substr in sp_details:
            if (substr == "."):
                break
            sp_index += substr
        
        desired_sp_idx = self.find_sub_task_by_index(self.active_project, int(sp_index))
        
        # initialize this sp so that we can use the "Add members" button.
        self.active_sp = self.active_project.sub_tasks[desired_sp_idx]
        
        # Each SP class holds data like so:
        #                       self.sp_dict[data[0]] = (data[1], data[2])
        #           OR,         IT has a dict that holds {person: (ETA, FinishDate)}
        # Also, I'm trying to invest in dogehouse before Microsoft acquires them.
        
        if (self.isLabel == True and self.table_widget != None):
            # There is a table on-screen, delete it first. 
            self.table_widget.deleteLater()
            self.table_widget = None

        if (self.active_sp.members == 0):
            # The reason we let the clear happen is because:
            # If I click SP X and it has 3 members, then sp Y and it has 0.
            # I want to delete X's table on-screen but return before showing something for Y.
            # self.isLabel doesn't need a bitswitch here.
            return
            
        self.table_widget = QTableWidget(self.centralWidget())
        self.table_widget.setRowCount(self.active_sp.members)       
        self.table_widget.setColumnCount(3)
        self.table_widget.move(950, 35)

        size_y = 30
        for idx, person in enumerate(self.active_sp.sp_dict):
            self.table_widget.setItem(idx, 0, QTableWidgetItem(person))
            self.table_widget.setItem(idx, 1, QTableWidgetItem(self.active_sp.sp_dict[person][0]))
            self.table_widget.setItem(idx, 2, QTableWidgetItem(self.active_sp.sp_dict[person][1]))
            size_y += 30
            
        # This stops scrolling and is consistent behavior across devices.
            # Because, we only have 3 items, thus the x value is same.
            # The Y value adjusts with the amount of entries.

        self.table_widget.setFixedSize(330,size_y)       
        self.table_widget.show()
        
        self.isLabel = True
 #       self.layout.addWidget(self.tableWidget)
    
    def add_new_member_to_sp(self):
        '''
        @Onclickevent for "Add Member"
        '''
        
        if (self.active_sp == None):
            my_Error.click_sp_first(self)
            return
                
        new_dialog = Dialog(self.active_project, default=False)
        ok_pressed = new_dialog.exec_()
            
        if (ok_pressed == 1):
            # return [team_member_name, eta, fin_date]
            data = new_dialog.extract_sp_data()    
        else:
            return
        
        self.active_sp.add_data(data)
        
    def show_sub_project_names(self, sub_project_list):
        '''
        A modification to the function below this function.
        This is more compact. Only shows the project's subproject names.
        
        Params: Array containing subprojects for THIS project.
        '''
        
        if (self.subproject_widgets != []):
            # There is already a bunch of subprojects on screen, delete them.
            for widget in self.subproject_widgets:
                widget.clicked.connect(self.doNothing)
                widget.deleteLater()
            
            self.subproject_widgets = []

        
        posy = 25
        for sp in sub_project_list:
            new_sp_btn = QPushButton(str(sp.idx) + ".\t" + sp.name, self)
            new_sp_btn.clicked.connect(self.connect_sp_keys)
            # The delete key above it is at (540,0)
            new_sp_btn.move(540, posy)
            new_sp_btn.resize(400, 35)
            posy += 35
            
            new_sp_btn.show()
            
            self.subproject_widgets.append(new_sp_btn)
            
        if (self.active_project != None):
            self.reload_delete_keys(self.active_project)

    
    def show_new_sub_project_clutter(self, string, project=None):
        '''
        A function to clear the subproject label on screen incase a new project is clicked.
        This shows a dirty label.
        
        
        It's useless now since I changed the SP class, I dont have the will to remove it. 
        It took me a while to write this.
        '''
        return
    
        if(self.isLabel):
            self.string_label.clear()
            self.isLabel = False

        self.string_label = QLabel(string, self)
        self.string_label.move(550,30)
        self.string_label.show()
        self.string_label.adjustSize()
        self.isLabel = True 

        if (project != None):
            self.reload_delete_keys(project)
    
    def new_project_window(self):                
        '''
        Think of this as @onclickevent for new project
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

        self.show_new_sub_project_clutter(new_project_sub_string)
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
        
        existing_project_btn.resize(520,50)
#        existing_project_btn.adjustSize()
        existing_project_btn.show()
        
        existing_project_btn.click()
        
        if (self.active_project_title == ""):
            self.active_project_title = new_project.name
            
        if (self.active_project == None):
            self.active_project = new_project
                
        # Just debugging here.
        self.manager.show_all()
        
        # The project on screen has changed, reload delete keys.
        self.reload_delete_keys(new_project)

    def add_new_project_button(self):
        '''
        Adds the "new project" button on to the screen
        Adds the "new sub project" button on to the screen
        
        This happens both in reinit or init.
        '''
        
        # This widget is the table seen when you click a SP.
        self.table_widget = None
        
        new_project_btn = QPushButton("New Project\n Click on a project and hold right-click for drag!", self)
        new_project_btn.move(0,0)
        new_project_btn.resize(100,20)
        new_project_btn.clicked.connect(self.new_project_window) 
   #     self.layout.addWidget(new_project_btn)


        change_project_data_btn = QPushButton("Edit This Project", self)
        change_project_data_btn.move(100,0)        
        change_project_data_btn.resize(100,20)
        change_project_data_btn.clicked.connect(self.edit_project)
        change_project_data_btn.show()


        new_sub_project_btn = QPushButton("New Sub-Project", self)
        new_sub_project_btn.move(200,0)
        new_sub_project_btn.resize(100,20)
        new_sub_project_btn.clicked.connect(self.add_sub_project_to_projects)


        delete_project_btn = QPushButton("Delete This Project", self)
        delete_project_btn.move(300,0)
        delete_project_btn.resize(100,20)
        delete_project_btn.clicked.connect(self.delete_project)
        
        
        
        add_members_btn = QPushButton("Add Members", self)
        add_members_btn.move(950, 0)
        add_members_btn.resize(100, 20)
        add_members_btn.clicked.connect(self.add_new_member_to_sp)

        delete_members_btn = QPushButton("Delete Members", self)
        delete_members_btn.move(1050, 0)
        delete_members_btn.resize(100, 20)


        edit_members_btn = QPushButton("Edit Members", self)
        edit_members_btn.move(1150, 0)
        edit_members_btn.resize(100, 20)
        

        # This adds a checkbox on the screen it will be removed later its just handy for debugging.
        # ----------------------- Debugging ------------------------------        
        self.debug_check = QCheckBox("New Window? [Debug]", self)
        self.debug_check.move(400,0)
        self.debug_check.adjustSize()
        self.debug_check.show()
        # ----------------------- Debugging ------------------------------
     
        
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
        
            
    def flush_delete_sp_buttons(self):
        '''
        A function to remove unnesscary widgets from screen when the last project is deleted or in ..
        .. specific scnearios.
        '''
                
        if (self.subproject_widgets != []):
            for widget in self.subproject_widgets:
                widget.clicked.connect(self.doNothing)
                widget.deleteLater()
            
            self.subproject_widgets = []

        if (self.delete_widgets != []):
            for widget in self.delete_widgets:
                widget.clicked.connect(self.doNothing)
                widget.deleteLater()
            
            self.delete_widgets = []

    def debug(self):
        print("Click me harder!")