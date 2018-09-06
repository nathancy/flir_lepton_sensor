from PyQt4 import QtGui, QtCore
from subprocess import call
import sys
import os

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 1000, 800)
        self.setWindowTitle("Flir")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

        # Create menubar
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")

        # Menubar options
        # Browse file system for CSV file
        open_CSV_file_action = QtGui.QAction("&Open CSV file", self)
        open_CSV_file_action.setShortcut("Ctrl+O")
        open_CSV_file_action.setStatusTip("Browse file system for CSV data file")
        open_CSV_file_action.triggered.connect(self.generate_KML_file)
        fileMenu.addAction(open_CSV_file_action)

        # Open latest CSV file
        open_latest_CSV_file_action = QtGui.QAction("&Convert latest CSV file", self)
        open_latest_CSV_file_action.setShortcut("Ctrl+L")
        open_latest_CSV_file_action.setStatusTip("Automatically select and convert latest CSV data file")
        open_latest_CSV_file_action.triggered.connect(self.generate_latest_KML_file)
        fileMenu.addAction(open_latest_CSV_file_action)
      
        # Close program
        exit_action = QtGui.QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Close program")
        exit_action.triggered.connect(self.close_application)
        fileMenu.addAction(exit_action)

        self.statusBar()
        self.home()

        self.KML_generator_latest_filename = "KML_generator_latest.py"
        self.KML_generator_filename = "KML_generator.py"


    def home(self):
        button = QtGui.QPushButton("Quit", self)
        button.clicked.connect(self.close_application)
        button.resize(100,100)
        button.move(100,100)
        self.show()

    # Menu option functions
    def generate_KML_file(self):
        CSV_file_path = QtGui.QFileDialog.getOpenFileName(self, 'Select CSV file', './', "Text files (*.csv)")
        call(["python", self.KML_generator_filename, CSV_file_path])

    def generate_latest_KML_file(self):
        call(["python", self.KML_generator_latest_filename])

    def close_application(self):
        sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()

