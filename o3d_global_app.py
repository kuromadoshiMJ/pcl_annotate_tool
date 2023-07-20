from PyQt6.QtWidgets import (QApplication, 
                             QWidget, 
                             QMainWindow, 
                             QPushButton, 
                             QGridLayout, 
                             QHBoxLayout, 
                             QVBoxLayout, 
                             QComboBox, 
                             QFileDialog,
                             QLineEdit,
                             QLabel)


import numpy as np
import open3d as o3d
import win32gui, win32con
from PyQt6 import QtGui
from PyQt6.QtGui import QAction
import pathlib
import laspy
# Only needed for access to command line arguments
import sys
import multiprocessing, threading
global_idx = []
global_points_label = []
global_current_pyqt_label = 0
global_change_label_clicked = 0
global_label_color_dict = {0:[1, 1, 0], 1:[1, 0, 0], 2:[0, 0, 1], 3:[0, 1, 0], 4:[0, 1, 1], 5:[1, 0, 1]}
global_file_name = ""
global_file_type = ""
global_change_file_name_flag = 0
global_reset_pointcloud_flag = 0
global_save_file_flag = 0
global_save_file_name = ""
global_pcd = o3d.geometry.PointCloud()
global_orig_pcd = o3d.geometry.PointCloud()
global_undo_stack = []
global_redo_stack = []
global_undo_flag = 0
global_redo_flag = 0

class MainWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)

        # create text field
        self.textfield = QLineEdit()
        self.textfield.setObjectName("Add Labels")
        # self.textfield.setFixedHeight(25)
        #create combobox
        self.combobox = QComboBox()
        self.labels_list = ['label1', 'label2', 'label3']
        self.label_dict ={'label1':1, 'label2':2, 'label3':3}        
        self.combobox.addItems(self.labels_list)
        self.combobox.setFixedWidth(200)
        self.combobox.setEditable(True)
        self.combobox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.current_pyqt_label = 0
        #crete change label buttoon
        self.button = QPushButton("Change Label")
        self.button.setFixedWidth(120)
        self.button.clicked.connect(self.click_change_labels)
        
        # create reset point cloud button
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedWidth(120)
        self.reset_button.clicked.connect(self.click_reset_pointcloud)

        # create Undo Button
        self.undo_button = QPushButton("Undo")
        self.undo_button.setFixedWidth(120)
        self.undo_button.clicked.connect(self.click_undo_button)
        # create redo Button
        self.redo_button = QPushButton("Redo")
        self.redo_button.setFixedWidth(120)
        self.redo_button.clicked.connect(self.click_redo_button)
        # create add label button
        self.add_button = QPushButton("Add Label")
        self.add_button.setFixedWidth(120)
        self.add_button.clicked.connect(self.click_add_labels)
        #create Action
        open_file_action = QAction("Open File", self)
        open_file_action.triggered.connect(self.open_file_dialog)

        save_file_action = QAction("Save File", self)
        save_file_action.triggered.connect(self.save_file_dialog)
        
        # Menu Bar
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)
        # Format Layout
        layout.addWidget(self.combobox)
        layout.addWidget(self.button)
        layout.addWidget(self.textfield)
        layout.addWidget(self.add_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.undo_button)
        layout.addWidget(self.redo_button)
        layout.addStretch()
        # layout.addWidget(self.button)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_file_dialog(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        # print(file_name)
        if file_name:
            global global_file_name
            global global_file_type
            global global_change_file_name_flag

            global_file_name = file_name
            global_file_type = pathlib.Path(file_name).suffix
            print(global_file_type)
            global_change_file_name_flag = 1
    def click_change_labels(self):
        print("works")
        cur_label_key = self.combobox.currentText()
        self.current_pyqt_label = self.label_dict[cur_label_key]
        global global_current_pyqt_label
        global_current_pyqt_label = self.current_pyqt_label
        global global_change_label_clicked
        global_change_label_clicked = 1
    def click_reset_pointcloud(self):
        global global_reset_pointcloud_flag
        global_reset_pointcloud_flag = 1
    def click_undo_button(self):
        global global_undo_flag
        global_undo_flag = 1
    def click_redo_button(self):
        global global_redo_flag
        global_redo_flag = 1
    def click_add_labels(self):
        new_label = self.textfield.text()
        self.labels_list.append(new_label)
        self.combobox.addItem(new_label)
        self.label_dict[new_label] = len(self.labels_list)
        self.textfield.setText("")

    def save_file_dialog(self):
        file_name= QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        print(file_name)
        global global_save_file_name
        global global_save_file_flag
        global_save_file_name = file_name[0]
        global_save_file_flag = 1




# Create a Qt widget, which will be our window.
def run_pyqt():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('App GUI')
    # window.setGeometry(100, 100, 400, 300)
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.
# Start the event loop.
    sys.exit(app.exec())

def call_back(v):
    global global_idx
    global global_current_pyqt_label
    global global_change_label_clicked
    global global_label_color_dict

    global global_file_name
    global global_file_type
    global global_change_file_name_flag
    global global_reset_pointcloud_flag
    global global_pcd
    global global_orig_pcd
    global global_save_file_flag
    global global_save_file_name
    global global_redo_flag
    global global_undo_flag
    global global_redo_stack
    global global_undo_stack
    idx = []
    idx = v.get_selected_points()

    if len(idx) > 0:
        global_idx = idx
        print("done")
        np.asarray(global_pcd.colors)[idx] *= np.array([0.8,0.8, 0.8])
        v.update_geometry(global_pcd)
        v.update_renderer()
        # colorarr = np.asarray(pcd.colors)
        # print("1col", np.asarray(pcd.colors)[:100])
    if len(global_idx)>0:
        # print("var stored", global_current_pyqt_label, global_change_label_clicked)  
        if global_change_label_clicked == 1:
            np.asarray(global_pcd.colors)[idx] *= np.array([1.25,1.25, 1.25])
            np.asarray(global_pcd.colors)[global_idx] = np.array(global_label_color_dict[global_current_pyqt_label])
            global_undo_stack.append([1, global_current_pyqt_label, global_idx])     
            global_change_label_clicked = 0

        # if global_current_pyqt_label == 1:
        #     np.asarray(pcd.colors)[idx] *= np.array([1,0, 0])
        # if global_current_pyqt_label == 2:
        #     np.asarray(pcd.colors)[idx] *= np.array([0,1, 0])
        # if global_current_pyqt_label == 3:
        #     np.asarray(pcd.colors)[idx] *= np.array([1,0, 1])
        # print("2col", np.asarray(pcd.colors)[:100])
            v.update_geometry(global_pcd)
            v.update_renderer()
    
    # open file
    if(global_change_file_name_flag == 1):
        print("File Opened")
        v.remove_geometry(global_pcd, False)
        if global_file_type == ".laz" or global_file_type == ".las":
            las_pcd = laspy.read(global_file_name)
            las_pcd_points = np.vstack((las_pcd.x, las_pcd.y, las_pcd.z)).transpose()
            las_pcd_colors = np.vstack((las_pcd.red, las_pcd.blue, las_pcd.green)).transpose()
            global_pcd = o3d.geometry.PointCloud()
            global_orig_pcd = o3d.geometry.PointCloud()
            global_pcd.points = o3d.utility.Vector3dVector(las_pcd_points)
            global_orig_pcd = o3d.utility.Vector3dVector(las_pcd_points)
            
        else:        
            global_pcd = o3d.io.read_point_cloud(global_file_name)
            global_orig_pcd = o3d.io.read_point_cloud(global_file_name)
        # global_orig_pcd = global_pcd
        points = np.asarray(global_pcd.points)
        # global_pcd.colors = o3d.utility.Vector3dVector(np.ones(points.shape))
        # np.asarray(global_pcd.colors)[:] = np.array([0.3,0.3,0.3])
        
        print(points.shape)
        global_change_file_name_flag = 0
        v.add_geometry(global_pcd)
        v.update_renderer()
    
    if(global_save_file_flag == 1):
        print("File Saved")
        o3d.io.write_point_cloud(global_save_file_name, global_pcd)
        global_save_file_flag = 0
    if(global_reset_pointcloud_flag == 1):
        v.remove_geometry(global_pcd, False)
        global_pcd = global_orig_pcd
        v.add_geometry(global_pcd)
        v.update_renderer()
        global_reset_pointcloud_flag = 0
    if(global_undo_flag == 1):
        # print(global_undo_stack)
        if(len(global_undo_stack)>=1):
            last_action = global_undo_stack[-1]
            last_idx = last_action[2]
            global_undo_stack.pop()
            np.asarray(global_pcd.colors)[last_idx] = np.array(global_orig_pcd.colors)[last_idx]
            global_redo_stack.append(last_action)
            v.update_geometry(global_pcd)
            v.update_renderer()
            print("undoed")
        global_undo_flag = 0
    if(global_redo_flag == 1):
        if(len(global_redo_stack)>=1):
            last_action = global_redo_stack[-1]
            last_idx = last_action[2]
            last_label = last_action[1]
            np.asarray(global_pcd.colors)[last_idx] = np.array(global_label_color_dict[last_label])
            global_redo_stack.pop()
            global_undo_stack.append()
            np.asanyarray(global_pcd)
if __name__ == '__main__':
    
    p = threading.Thread(target=run_pyqt, args=())
    p.start()
    print("process started")
    dataset = o3d.data.PCDPointCloud()
    # global global_pcd
    # global_pcd = o3d.io.read_point_cloud(dataset.path)
    # points = np.asarray(global_pcd.points)
    # print(points.shape)
    
    
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(global_pcd)
    vis.register_animation_callback(call_back)
    vis.run()
    p.join()
