# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 01:43:40 2021

@author: garvi
"""

from PyQt5.QtWidgets import  (QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout, \
                             QLabel, QLineEdit,\
                             QVBoxLayout, QWidget, QCheckBox)

from my_error import my_Error
# Lol I wrote this i forgot what it does.
# NOte to self: This is the dialog class for "EDIT PROJECT"

class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, active_project, default = "Default"):
        super(Dialog, self).__init__()
        
        self.preference = default
        #NOTE:
            # This is slightly misleading, but active_project can hold PROJECT OR SUBPROJECT.
            # The dialogs vary base on user_input, edit_sp, delete_sp, add_sp dont use active_project,
            # In that scope, active_project is meta-data relating to the subproject class.
        self.active_project = active_project
 
        if (default == "Default"):
            # To avoid de duplication, this smae code block is reused when a user adds team members to SPs
            # for a given project.
            
            # Define SP: Sub-project
            self.create_group_box()    
        elif (default == "Add"):
            self.create_group_box_add_members()
        elif (default == "Edit"):
            self.create_group_box_edit_members()
        elif (default == "Delete"):
            self.create_group_box_delete_members()
        else:
            # The code is not supposed to get here ever.
            my_Error.unexpected_catch(self)
            return
                
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(btn_box)
        self.setLayout(main_layout)
        
        self.setWindowTitle("Change Project - {}".format(self.active_project.name))

        
    def create_group_box(self):
        self.form_group_box = QGroupBox("{}".format(self.active_project.name))
            
        self.new_sub_task_names_array = []
        self.layout = QFormLayout()
        
        self.new_project_name = QLineEdit()
        self.layout.addRow(QLabel("New Project Name:"), self.new_project_name)
        # This is like a new line, im really smart lol.
        self.layout.addRow(QLabel(""))
        
        
        # indices is a word? Yeah no we speak my english here.
        sub_task_indexes = []
        for subprojects in self.active_project.sub_tasks:
            self.new_sub_task_name = QLineEdit()
            self.new_sub_task_name.setPlaceholderText("Name of Subtask")

            self.layout.addRow(QLabel("New Name of Idx {}:".format(str(subprojects.idx))), self.new_sub_task_name)
            
            self.new_sub_task_names_array.append(self.new_sub_task_name)

            sub_task_indexes.append(str(subprojects.idx))
            
        
        self.new_project_name.setPlaceholderText(self.active_project.name)

        self.form_group_box.setLayout(self.layout)
        
        self.move(230, 90)
                
    def create_group_box_add_members(self):
        '''
        Does exactly the same as below but for adding members to a SP.
        
        The "Add-Members" button on the screen.
        '''
        self.form_group_box = QGroupBox("{}".format(self.active_project.name))
        
        if (self.preference == "Add"):
            self.team_member_name = QLineEdit()
        else:
            # self.prefernece == "Edit" here.
            self.team_member_name = QComboBox()
            
        self.eta_options = QComboBox()
        self.eta_raw_value = QLineEdit()
        self.fin_date = QLineEdit()

        self.layout = QFormLayout()        
        # This is a bit complicated so I'll explain for future-me:
            # TL;DR addRow doesnt have a method for 3 widgets.
            # Thus you use nested widget + 1 widget for the 2-widget method.        
        hBoxLayout = QHBoxLayout()
        hBoxLayout.addWidget(self.eta_raw_value)
        hBoxLayout.addWidget(self.eta_options)
        
        self.container_of_eta = QWidget()
        self.container_of_eta.setLayout(hBoxLayout)

        # This is my desire to not deduplicate code.
        # Add and edit are very similar.
        # To make life easier, it's much easier to edit a member with a combo box, not a line edit.
        # Edit and Add both call this function.
            # Use default to "swap" between which one we want.
        
        if (self.preference == "Add"):
            self.layout.addRow(QLabel("New Team-Member Name:"), self.team_member_name)
        else:
            # It will be self.preference == "Edit" here.
            # This is not redudant, it's done on purpose so it's easier to understand there is a difference.
            # Between add and edit.
            
            # self.team_member_name here is a QComboBox to make editing a member easier.
            self.layout.addRow(QLabel("Edit This Team-Member:"), self.team_member_name)
            self.team_member_name.clear()
            
            # self.active_project is self.active_sp here. 
            # Each SP has a dictionary containing the people: (eta, fin_date) as data.
            # So grab the keys as a list, popualate the list.
            self.team_member_name.addItems(list(self.active_project.sp_dict.keys()))

            
        self.layout.addRow(QLabel("\nNew ETA: "), self.container_of_eta)
        self.layout.addRow(QLabel("New Finish Date:"), self.fin_date)
        
        self.eta_options.clear()
        self.eta_options.addItems(['Minutes', 'Hours', 'Days', 'Months', 'Years'])
        
        if (self.preference == "Add"):
            self.team_member_name.setPlaceholderText("Name of Member")
        
        # No else, there is no placeholder for Combo boxes.
        self.fin_date.setPlaceholderText("01/01/2022")
        self.eta_raw_value.setPlaceholderText('0')
        self.form_group_box.setLayout(self.layout)
        
    
    def create_group_box_edit_members(self):
        '''
        I'm reusing the same class for 3 different dialogues.
        This is for "Edit-Members"
        
        The reason why this is a new function is because if I come back here in the future and see add_members
        I'll be confused AF.
        
        But reusing it is possible since it's literally the same data, it's just the SP class has an edit_function.
        to change existing data.
        '''
        self.create_group_box_add_members()
        
    
    def create_group_box_delete_members(self):
        self.form_group_box = QGroupBox("{}".format(self.active_project.name))
        
        self.layout = QFormLayout()
    
        self.layout.addRow(QLabel("Choose The Members: "))
        
        # Unique just to this TYPE of dialog, thus no point putting it in init.
        self.check_box_array = []
        
        # Members exist in self.active_project because in this scope, when called from gui.py,
        # self.active_project is self.active_sp.
        # Read the init function.
                                    # The sp_dict contains {person: (eta, fin_date)} thus the eta_fin_tuple
        for _, person in enumerate(self.active_project.sp_dict):
            new_check_box = QCheckBox()
            self.layout.addRow(QLabel("{}".format(person)), new_check_box)
            
            # Save the data in a checkbox array as person, check_box so it's easier to figure out,
            # What checkbox was ticked to delete which Member.
            desired_tuple = (person, new_check_box)
            self.check_box_array.append(desired_tuple)
        
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
        i, j = self.layout.getWidgetPosition(widget_name)
        widget_item = self.layout.itemAt(i, j)
        widget = widget_item.widget()
        
        return widget.currentText()
    
    def extract_container(self, widget_name):
        i, j = self.layout.getWidgetPosition(widget_name)
        widget_item = self.layout.itemAt(i, j)
        widget = widget_item.widget()
        
        eta_raw_value = ""
        eta_option_chosen = ""
        
        children = widget.children()
            # 1 is the line edit, 2 is the combo box.
            # This remains consistent since it's a UI thing.
            
            # IF it causes issues I can always do a typecheck. But it really wont unless Qt5 changes their stuff
        eta_raw_value = children[1].text()
        eta_option_chosen = children[2].currentText()
        
        return (eta_raw_value + " " + eta_option_chosen)
        
    def extract_data(self):        
        # Get the new project name
        ret = []
        new_project_name = self.extract_qline(self.new_project_name)
        ret.append(new_project_name)
        
        for new_sub_task_names in self.new_sub_task_names_array:
            new_sub_task_name = self.extract_qline(new_sub_task_names)
            ret.append(new_sub_task_name)
            
        return ret
    
    def extract_data_for_deletion(self):
        '''
        The deletion dialog is substantially different from add/edit,
        Thus we need to do sick stuff.
        '''
        persons_to_delete =[]
        for doublets in self.check_box_array:
            # Doublets are (person, QCheckBox()) in this array.
            if (doublets[1].isChecked() == True):
                persons_to_delete.append(doublets[0])
            
        return persons_to_delete

    def extract_sp_data(self):
        '''
        A function like above, but extract SP data.
        '''
        if (self.preference == "Add"):
            team_member_name = self.extract_qline(self.team_member_name)
        else:
            # will be self.preferecne == "Edit" here
            team_member_name = self.extract_qbox(self.team_member_name)
        eta = self.extract_container(self.container_of_eta)
        fin_date = self.extract_qline(self.fin_date)

        return [team_member_name, eta, fin_date]