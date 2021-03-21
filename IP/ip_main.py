# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 21:58:35 2021

@author: garvit
"""

import sys
import gui as gui

from project import Project
from project_manager import Project_Manager

# -=============================
import test2 as t2
# -=============================

from os import path

def dbug(new_project):
    print ("-" * 20)
    print(new_project.name)
    print ("-" * 20)
    print(new_project.is_active, "[Is Active?]")    
    print ("-" * 20)
    
    print ("\n\nSub-Tasks:")
    
    print(new_project.sub_tasks[0].name)
    print ("-" * 20)
    print(new_project.sub_tasks[0].eta, "Minutes (Time Left)")
    print ("-" * 20)
    print(new_project.sub_tasks[0].finish_date)
    print ("-" * 20)
    print(new_project.sub_tasks[0].members)


if __name__ == "__main__":
    print ("Hi!\n")
    
    
        
    # init a new project.
    new_project = Project()    
        
    # Make a project manager object.
    project_manager = Project_Manager()
    
    # Setup and show the main window.
    construct_application = t2.QApplication(sys.argv)
    app_object = t2.Main_Screen(project_manager)
    
    # Mainly for debugging on terminal.
    project_manager.show_all()
           
    # Exit safely.
    sys.exit(construct_application.exec_())
    
        