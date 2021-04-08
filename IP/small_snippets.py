from sys import exit as sysExit

from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.LaidOut = QFormLayout()
        self.Entry = QLineEdit()
        self.LaidOut.addRow(self.Entry, QLineEdit())

        self.setLayout(self.LaidOut)

        ePos = self.LaidOut.getWidgetPosition(self.Entry)
        print('EPos :',ePos)
#        text = self.LaidOut.itemAt(ePos[1],ePos[0]+1).text()
        print('Text :',self.LaidOut.itemAt(ePos[1],ePos[0]+1).isEmpty())

if __name__ == "__main__":
    MainThred = QApplication([])

    MainGUI = MainWindow()
    MainGUI.show()
    sysExit(MainThred.exec_())
