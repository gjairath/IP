# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 00:35:13 2021

@author: garvi
"""


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt


class Canvas(FigureCanvas):
    def __init__(self, active_project, parent = None, width = 5, height = 5, dpi = 100):
        
        fig, self.axes = plt.subplots(figsize=(4.8, 4.8))
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.plot()


    def plot(self):
        x = np.array([50, 30,40])
        labels = ["Apples", "Bananas", "Melons"]
        ax1 = self.figure.add_subplot(111)
        ax1.pie(x, labels=labels, autopct=None, shadow=False, startangle=90)
        ax1.axis("off")

        
        fig, ax = plt.subplots(figsize=(4.8, 4.8))
        ax.pie(x, autopct=None, shadow=False, startangle=90)
        fig.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        ax.axis('equal')
        ax.margins(0, 0)
        
        fig.show()
