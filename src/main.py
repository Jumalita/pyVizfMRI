import sys

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QToolBar, QStatusBar, \
    QFileDialog, QDialog
from PySide6.QtGui import QPalette, QColor, QAction, QIcon

import pyqtgraph as pg

import numpy as np

from pathlib import Path

from fMRI_Obs import FC

import fMRI_Obs.BOLDFilters as filters

from src.dialogs.define_interval import DefineInterval
from src.widgets.bold_widget import BOLD
from src.widgets.fct_widget import FCtHeatMap
from src.widgets.heatmap_widget import HeatMap

filters.k = 2       # 2nd order butterworth filter
filters.flp = .008  # lowpass frequency of filter
filters.fhi = .08   # highpass
filters.TR = 0.754  # sampling interval

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class FCHeatMap(QDialog):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle("Functional connectivity")

        self.layout = QVBoxLayout()
        self.layout.addWidget(HeatMap(np.corrcoef(data)))
        self.setLayout(self.layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.tab_names = {}

        self.setWindowTitle("BOLD analyzer")

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(True)

        self.setCentralWidget(self.tabs)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("../bug.png"), "&Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.compute_fc)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        self.setStatusBar(QStatusBar(self))
        menu = self.menuBar()

        # File menu
        file_menu = menu.addMenu("&File")

        open_file_action = QAction(QIcon("../folder-open-document.png"), "Open file", self)
        open_file_action.setStatusTip("Open NPY file")
        open_file_action.triggered.connect(self.open_file)

        file_menu.addAction(open_file_action)

        self.dialog = QFileDialog(self)

        self.dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.dialog.setWindowTitle('Open NPY file...')
        self.dialog.setNameFilter("NPY files (*.npy)")

        self.dialog.finished.connect(self.on_open_file_finished)

        # Observables menu
        obs_menu = menu.addMenu("&Observables")

        fc_action = QAction(QIcon("../gear.png"), "FC", self)
        fc_action.setStatusTip("Compute FC")
        fc_action.triggered.connect(self.compute_fc)

        obs_menu.addAction(fc_action)

        swfc_action = QAction(QIcon("../gear.png"), "FC(t)", self)
        swfc_action.setStatusTip("Compute FC(t)")
        swfc_action.triggered.connect(self.add_fct_plot)

        obs_menu.addAction(swfc_action)

        # Tools menu
        tools_menu = menu.addMenu("&Tools")

        fc_action = QAction(QIcon("../gear.png"), "Set y limits", self)
        fc_action.setStatusTip("Set y limits")
        fc_action.triggered.connect(self.adjust_ylim)

        tools_menu.addAction(fc_action)

        fc_action = QAction(QIcon("../gear.png"), "Auto-adjust y limits", self)
        fc_action.setStatusTip("Auto-adjust y limits")
        fc_action.triggered.connect(self.adjust_ylim_auto)

        tools_menu.addAction(fc_action)

    def compute_fc(self, s):
        cw = self.tabs.currentWidget()
        m = FC.from_fMRI(cw.data.T)
        dlg = FCHeatMap(m)
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")

    def draw_window(self, x, w):
        ly, cw = self.tab_names[self.tabs.tabText(self.tabs.currentIndex())]
        cw.plot_window(x, w)

    def add_fct_plot(self, s):
        ly, cw = self.tab_names[self.tabs.tabText(self.tabs.currentIndex())]
        w_fct = FCtHeatMap(cw.data.T, self.draw_window)
        ly.addWidget(w_fct, stretch=4)

    def open_file(self):
        filenames, _ = QFileDialog.getOpenFileNames(
            parent=self,
            caption="Select Files",
            filter="NPY files (*.npy)"
        )
        if filenames:
            for file in filenames:
                data = np.load(file)
                if len(data.shape) == 3:
                    for i in range(0, data.shape[0]):
                        suffix = f"_{i}" if data.shape[0] > 1 else ""
                        self.add_bold_plot(data[i], Path(file).stem + suffix)
                elif len(data.shape) == 2:
                    self.add_bold_plot(data, Path(file).stem)

    def on_open_file_finished(self, ein):
        for file in self.dialog.selectedFiles():
            data = np.load(file)
            if len(data.shape) == 3:
                for i in range(0, data.shape[0]):
                    suffix = f"_{i}" if data.shape[0] > 1 else ""
                    self.add_bold_plot(data[i], Path(file).stem + suffix)
            elif len(data.shape) == 2:
                self.add_bold_plot(data, Path(file).stem)

    def add_bold_plot(self, data, name):
        w = BOLD(data)
        self.add_tab(w, name)

    def add_tab(self, w_bold, name):
        w = QWidget()
        ly = QHBoxLayout()
        ly.addWidget(w_bold, stretch=10)
        w.setLayout(ly)
        self.tabs.addTab(w, name)
        self.tab_names[name] = (ly, w_bold)

    def adjust_ylim(self):
        id = DefineInterval("Define Y limits", "Y Limits", 0, 1)
        if id.exec():
            for _, (_, w_bold) in self.tab_names.items():
                w_bold.set_ylim(id.min_max[0], id.min_max[1])

    def adjust_ylim_auto(self):
        ymin = 1e6
        ymax = -1e6
        for _, (_, w_bold) in self.tab_names.items():
            range = w_bold.getViewBox().viewRange()
            y0 = range[1][0]
            y1 = range[1][1]
            if y0 < ymin:
                ymin = y0
            if y1 > ymax:
                ymax = y1

        for _, (_, w_bold) in self.tab_names.items():
            w_bold.set_ylim(ymin, ymax)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()