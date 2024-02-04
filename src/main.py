import sys
import numpy as np
import scipy.io as sio
import nibabel as nib
from PySide6.QtWidgets import (QApplication,
                               QMainWindow,
                               QTabWidget,
                               QToolBar,
                               QMessageBox,
                               QFileDialog)
from PySide6.QtGui import QAction
from pathlib import Path

from widgets.DataTab import DataTab


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tab_names = {}

        self.setWindowTitle("fMRI Visualizer")

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.delete_data_tab)
        self.tabs.setTabsClosable(True)

        self.setCentralWidget(self.tabs)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")

        open_file_action = QAction("Open file", self)
        open_file_action.triggered.connect(self.open_file)

        file_menu.addAction(open_file_action)

    def open_file(self):
        filenames, _ = QFileDialog.getOpenFileNames(
            parent=self,
            caption="Open NPY/Mat/Nii/TXT files...",
            filter="fMRI files (*.npy *.mat *.nii *.txt)"
        )
        if filenames:
            for file in filenames:
                if file.endswith(".mat"):  # TODO: recheck
                    data = sio.loadmat(file)['fc_s0003']
                elif file.endswith(".nii"):
                    img = nib.load(file)
                    data = img.get_fdata()
                elif file.endswith(".npy"):
                    data = np.load(file)
                elif file.endswith(".txt"):
                    result = []
                    with open(file, 'r') as stream:
                        lines = stream.readlines()
                        for line in lines:
                            values = [float(val) for val in line.strip().replace(' ', '\t').split('\t')]
                            result.append(values)
                    data = np.array(result)
                else:
                    raise ValueError("Reading file with incorrect format")

                if len(data.shape) == 3:
                    for i in range(0, data.shape[0]):
                        suffix = f"_{i}" if data.shape[0] > 1 else ""
                        self.add_data_tab(data[i], Path(file).stem + suffix)
                elif len(data.shape) == 2:
                    self.add_data_tab(data, Path(file).stem)

    def add_data_tab(self, data, name):
        tab = DataTab(data, name)
        self.tabs.addTab(tab, name)
        # self.tab_names[name] = w
    def delete_data_tab(self,index):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Alert!")
        dlg.setText("Closing this tab will make you lose your work and its corresponding dialogs. Cointinue?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        if button == QMessageBox.Yes:
            self.tabs.widget(index).before_close()
            self.tabs.removeTab(index)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
