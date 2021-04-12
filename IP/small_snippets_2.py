import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

class UserInterface(QMainWindow):

    def __init__(self):
        super(UserInterface, self).__init__()

        self.table_widget = MyTable()

        self.widget = QWidget(self)
        layout = QGridLayout()
        self.widget.setLayout(layout)
        layout.addWidget(self.table_widget)
        layout.addWidget(close_button)

        self.setCentralWidget(self.widget)

class MyTable(QWidget):

    def __init__(self):
        super(MyTable, self).__init__()
        self.Table()

    def Table(self):
        self.mytable()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.show()

    def mytable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setItem(0, 0 , QTableWidgetItem("Hello"))
        self.tableWidget.move(300, 300)


def Main():
    qapplication_constructor = QApplication(sys.argv)
    gui = UserInterface()
    gui.show()
    sys.exit(qapplication_constructor.exec_())

if __name__ == "__main__":
    Main()
