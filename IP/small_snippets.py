import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QDesktopWidget, \
                            QInputDialog, QCheckBox, QShortcut, QWidget, QGridLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QKeySequence, QDrag, QFont
from PyQt5.QtCore import Qt, QMimeData

name_data = ['ye', "Ye's brother", "Ye's mother", '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', "Ye's Cunt"] 
tuple_data = [('535 Minutes', ''), ('69 Minutes', ''), ('69 Minutes', '5353'), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', ''), (' Minutes', '')] 

hour_data_for_names = []
new_name_data = []
for idx, value in enumerate(tuple_data):
    num_hours = value[0].split(' ')[0]
    if (num_hours.isnumeric()):
        hour_data_for_names.append(int(num_hours) / 60)
        new_name_data.append(name_data[idx])


hours_left = 673 / 60        
print (hour_data_for_names, new_name_data, hours_left)

# Free memory    
name_data.clear()
tuple_data.clear()

import matplotlib.pyplot as plt
# Pie chart
labels = ['Frogs', 'Hogs', 'Dogs', 'Logs']
sizes = [15, 30, 45, 10]
#colors
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
 
fig1, ax1 = plt.subplots()
ax1.pie(hour_data_for_names, colors = colors, labels=new_name_data, autopct='%1.1f%%', startangle=90)

#draw circle
centre_circle = plt.Circle((0,0),0.70,fc='lightgrey')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
fig.set_facecolor('lightgrey')

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')  
plt.tight_layout()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        
        self.plot_widget = QWidget(self._main)
        self.plot_widget.setGeometry(250,180,500,600)
        

        static_canvas = FigureCanvas(fig)
        self.addToolBar(NavigationToolbar(static_canvas, self))

        plot_box = QtWidgets.QVBoxLayout()
        plot_box.addWidget(static_canvas)
        self.plot_widget.setLayout(plot_box)
#        self.table_widget = QTableWidget(self.centralWidget())


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
