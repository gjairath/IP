# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 00:20:48 2021

@author: garvi
"""


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSettings


class QMainWindow(QtWidgets.QMainWindow):
    comp_name = 'IP_inc'
    software_name = 'IP'
    settings_ui_name = 'User Settings'
    settings_ui_user_name = 'user'
    
    names_to_avoid = {}

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        
        # init a QSettings object to begin saving
        self.settings = QSettings(self.comp_name, self.software_name)
        self.counter = 1
        print(self.settings.fileName()) 
        
        
        self.restored_array = self.restore()
        
    def closeEvent(self, e):
        #self._gui_save()
        if (self.restored_array != []):
            names_to_avoid = [x[0] for x in self.restored_array]
        else:
            names_to_avoid = []
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
                        obj.setObjectName("button__{}".format(self.counter))
                        child_name = obj.objectName()
                        
                        child_text = obj.text()
                        if (child_text == "New Project"):
                            continue
                        
                        if (btns_to_avoid != [] and child_text in btns_to_avoid):
                            continue
                        
                        # Store as much info as you can about this button it can help later lol
                        #self.settings.beginWriteArray(child_name)
                        self.counter += 1
                        value = None              
                        value = [obj.text(), obj.geometry(), obj.size(), child_name]
                        
                    if value is not None:
                        self.settings.setValue(name_prefix + child_name, value)

    def split_N(self, source, step):   
        return [source[i::step] for i in range(step)]

    def restore(self):
       '''
       This function is harder than it seems with almost 0 documentation.
       I'm just going to use keys to extract the values and just go from there.
       
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

