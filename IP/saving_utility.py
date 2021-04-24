# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 00:20:48 2021

@author: garvi
"""


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSettings
import pickle

import os

class QMainWindow(QtWidgets.QMainWindow):
    comp_name = 'IP_inc'
    software_name = 'IP'
    settings_ui_name = 'User Settings'
    settings_ui_user_name = 'user'
    
    names_to_avoid = {}

    def __init__(self, project_manager, parent=None):
        super(QMainWindow, self).__init__(parent)
        
        # init a QSettings object to begin saving
        self.settings = QSettings(self.comp_name, self.software_name)
        self.counter = 1
        print(self.settings.fileName()) 
        
        
        ra = self.restore()
        self.restored_array = []

        if (ra != []):
            for i in ra: 
                if i not in self.restored_array:                     
                    self.restored_array.append(i) 
        
        # A project manager object that holds mostly project-subproject bridge abstracted away safely.
        self.manager = project_manager
        
        
        self.save_counter = 0
    

    def save_sub_projects(self):
        
        self.save_backups()

        # Project manager has QPushButtons which cannot be pickled.
        # However since self.save() saves the button objects, I can replace the buttons with 1, 2, 3, .. n. since the ...
        # ... Labels are saved like so. That should work basically the same.
        
        # Upon reconstruction, the text can be replaced with buttons once again to basically have the same thing.
        
        #key = (project, window, self.positionx, self.positiony)
        dict_projects = self.manager.projects
        new_dict = {}
        
        dict_keys = list(dict_projects.keys())

        i = 0
        for key in dict_projects.copy():
            # Take existing dict with a mapping and replace it with a placeholder.
            
            # First replace the tuple's window instance because it cannot be pickled by pickle.
            
            # This is dumb but it's okay because append has constant time complexity AND the tuple only has 4objects.
            placeholder_tuple = dict_projects[key]
            empty_list = []
            empty_list.append(placeholder_tuple[0])
            empty_list.append(placeholder_tuple[2])
            empty_list.append(placeholder_tuple[3])
                        
            # Now replace it as (project, self.posx, self.posy)
            # So we hold the data for the project, we have all the labels reinit'ed, reinit the windows and it should...
            # work.
            new_dict[dict_keys[i].text()] = tuple(empty_list)

            # Let garbage collector dereference this
            del dict_projects[key]            
            i += 1
        
        print (new_dict)
        pickle.dump(new_dict, open("subproj.dat", "wb"))                
        
        
    def closeEvent(self, e):
        #self._gui_save()
        if (self.restored_array != []):
            names_to_avoid = [x[0] for x in self.restored_array]
        else:
            names_to_avoid = []
        
        self.save_sub_projects()
        self.save(names_to_avoid)
        
    def get_handled_types(self):
        return [QPushButton]

    def save(self, btns_to_avoid):
        """
        save "ui" controls and values to registry "setting"
        
        btns_to_avoid: buttons already saved dont save them again, it causes fascinating behavior like terminator 2
                        if first time loading or there are no buttons, its empty list.
        :return:
        """
        name_prefix = f"{self.settings_ui_name}/"
        self.settings.setValue(name_prefix + "geometry", self.saveGeometry())

        for child in self.get_handled_types():
            for obj in self.findChildren(child):
                # If child = QPushButton, it returns all the current children of button instances.
                # obj are just values from this array above.
                
                if (obj):
                    if isinstance(obj, QPushButton):
                        obj.setObjectName("button__{}".format(self.save_counter))
                        child_name = obj.objectName()
                        
                        child_text = obj.text()
                        
                        if (child_text.find("+") != -1):
                            pass
                        else:
                            continue
#                        if (child_text == "New Project\n Click on a project and hold right-click for drag!" or child_text == "New Sub-Project" or child_text.startswith('Delete')\
 #                           or child_text.startswith('Edit')):
  #                          continue
                        
                        if (btns_to_avoid != [] and child_text in btns_to_avoid):
                            self.save_counter += 1
                            continue
                        
                        self.counter += 1
                        value = None              
                        value = [obj.text(), obj.geometry(), obj.size(), child_name]
                        
                    if value is not None:
                        self.settings.setValue(name_prefix + child_name, value)
                        self.save_counter += 1
                        
                                    
    def split_N(self, source, step):   
        return [source[i::step] for i in range(step)]

    def restore(self):
       '''
       This function is harder than it seems with almost 0 documentation.
       
       Params: none
       Returns: A list that contains lists of object attributes for all buttons only.
               Buttons cannot be pickled, and saving them is a pain.
               It is done through QSettings class.
               
       '''
       button_id = "button__" #each button value is identified with button when saving locally.
       
       # This function of QSetting remembers all keys in the HKEY directory.
       key_list = self.settings.allKeys() 
       
       # Contains all the keys with "button" there WILL be some redudancies.
       ret = [i for i in key_list if button_id in i]
       
       ret_val = [self.settings.value(i) for i in ret]
              
       return ret_val


    def add_setting(self, name, value):
        name_prefix = f"{self.settings_ui_user_name}/"
        self.settings.setValue(name_prefix + name, value)

    def get_setting(self, name):
        name_prefix = f"{self.settings_ui_user_name}/"
        return self.settings.value(name_prefix + name)
    
    
    def save_backups(self):
        '''
        In event of a failure which is unlikely due to amazing programming skills (moi)
        Just save stuff in a text file
        
        This function is funny because I wanted to replace the same wordpad I've been using for my own planning
        for so long.
        '''
        try:
            curr_dir = os.getcwd()

            if(os.path.exists(curr_dir + "/backups") == False):
                os.mkdir(curr_dir + "/backups")
            

            save_path = curr_dir + "/backups"
            save_file_name = "backups.txt"
    
            file_name_in_path = os.path.join(save_path, save_file_name)
            out_file_o = open(file_name_in_path, "w")
            
            for buttons in self.manager.projects:
                project_name = buttons.text()
                        # Projects:             A Dictionary that contains {button: (projects, window, x, y)}
                out_file_o.write("=====================\n")
                out_file_o.write(project_name)
    
                for subprojects in self.manager.projects[buttons][0].sub_tasks:
                    out_file_o.write("\n\n" + str(subprojects.idx) + ". ")
                    out_file_o.write(subprojects.name + "\t")
                    out_file_o.write("Num_Members:" + str(subprojects.members) + "\n")
                    
                    if (subprojects.sp_dict == {}): continue
                    out_file_o.write("\n")
                    for members in subprojects.sp_dict:
                        out_file_o.write("\t\t" + members)
                        out_file_o.write("\t\t" + subprojects.sp_dict[members][0] + "\t\t" + subprojects.sp_dict[members][1])
                        out_file_o.write("\n")
                        
        except:
            print ("Failed to backup")