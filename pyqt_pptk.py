from PyQt6 import QtWidgets, QtGui
import numpy as np
import pptk
import win32gui
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        button = QtWidgets.QPushButton("Press Here")
        self.setCentralWidget(button)
        # widget = QtWidgets.QWidget()
        # layout = QtWidgets.QGridLayout(widget)
        # self.setCentralWidget(widget)

        # self.cloudpoint = np.random.rand(100, 3)
        # self.v = pptk.viewer(self.cloudpoint)
        # hwnd = win32gui.FindWindowEx(0, 0, None, "viewer")
        # self.window = QtGui.QWindow.fromWinId(hwnd)    
        # self.windowcontainer = self.createWindowContainer(self.window, widget)

        # layout.addWidget(self.windowcontainer, 0, 0)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle("fusion")
    window = MainWindow()
    # window.setWindowTitle('PPTK Embed')
    # window.setGeometry(100, 100, 600, 500)
    window.show()
    app.exec_()