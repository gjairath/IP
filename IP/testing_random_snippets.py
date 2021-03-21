# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 00:20:48 2021

@author: garvi
"""


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSettings
from distutils.util import strtobool

import inspect


class QMainWindow(QtWidgets.QMainWindow):
    companie_name = 'CompanieName'
    software_name = 'SoftwareName'
    settings_ui_name = 'defaultUiwidget'
    settings_ui_user_name = 'user'
    _names_to_avoid = {}

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.settings = QSettings(self.companie_name, self.software_name)
        self.counter = 1
        print(self.settings.fileName()) 
        
    def closeEvent(self, e):
        self._gui_save()

    @classmethod
    def _get_handled_types(cls):
        return [QPushButton]

    @classmethod
    def _is_handled_type(cls, widget):
        return any(isinstance(widget, t) for t in cls._get_handled_types())


    def _gui_save(self):
        """
        save "ui" controls and values to registry "setting"
        :return:
        """
        name_prefix = f"{self.settings_ui_name}/"
        self.settings.setValue(name_prefix + "geometry", self.saveGeometry())

        for child in self._get_handled_types():
            for obj in self.findChildren(child):
                # If child = QPushButton, it returns all the current children of button instances.
                # obj are just values from this array above.
                
                if (obj):
                    if isinstance(obj, QPushButton):
                        obj.setObjectName("button{}".format(self.counter))
                        child_name = obj.objectName()
                        
                        # Store as much info as you can about this button it can help later lol
                        self.settings.beginWriteArray(child_name)
                        self.counter += 1
                        value = None
                        # Get button text.
                        self.settings.setArrayIndex(0)
                        self.settings.setValue("text", obj.text())
                        
                        # Get button geometry.
                        self.settings.setArrayIndex(1)
                        self.settings.setValue("geometry", obj.geometry())
                        
#                        value = [obj.text(), obj.geometry()]

                        self.settings.endArray()

                    if value is not None:
                        self.settings.setValue(name_prefix + child_name, value)

    def _gui_restore(self):
        """
        restore "ui" controls with values stored in registry "settings"
        :return:
        """

        name_prefix = f"{self.settings_ui_name}/"
        geometry_value = self.settings.value(name_prefix + "geometry")
        if geometry_value:
            self.restoreGeometry(geometry_value)

        for child in self._get_handled_types():
            for obj in self.findChildren(child):
                if (obj):

                    child_name = obj.objectName()
                    value = None
        
                    if isinstance(obj, QPushButton):
                        size = self.settings.beginReadArray(name_prefix + child_name)
                        for i in range(size):
                            self.settings.setArrayIndex(i)
                            value = self.settings.value(name_prefix + child_name)
                            if value is not None:
                                obj.addItem(value)
                        self.settings.endArray()

    def _add_setting(self, name, value):
        name_prefix = f"{self.settings_ui_user_name}/"
        self.settings.setValue(name_prefix + name, value)

    def _get_setting(self, name):
        name_prefix = f"{self.settings_ui_user_name}/"
        return self.settings.value(name_prefix + name)

