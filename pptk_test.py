import numpy as np
import pptk
import win32gui
import PyQt6 as Apple

# from PyQt5 import QtGui

x=np.random.rand(100, 3)

v=pptk.viewer(x)
print("working")
v.set(point_size=0.01)
print("hello")
# app = PyQt5.QtWidgets.QApplication([])
v.set()