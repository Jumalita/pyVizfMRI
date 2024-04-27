import sys
import csv
import numpy as np
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
        # Files accepted will be CSV
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open CSV files...",
            filter="fMRI files (*.csv)"
        )
        if filename:
            data = []
            if filename.endswith(".csv"):
                with open(filename, 'r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        row = [float(value) for value in row]
                        data.append(row)
            else:
                raise ValueError("Reading file with incorrect format")

            self.add_data_tab(np.array(data), Path(filename).stem)

    def add_data_tab(self, data, name):
        tab = DataTab(data, name)
        self.tabs.addTab(tab, name)

    def delete_data_tab(self, index):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Alert!")
        dlg.setText("Closing this tab will make you lose your work and its corresponding dialogs. Continue?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        if button == QMessageBox.Yes:
            self.tabs.widget(index).before_close()
            self.tabs.removeTab(index)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
