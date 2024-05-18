import sys
import csv
import numpy as np
from PySide6.QtWidgets import (QApplication,
                               QMainWindow,
                               QTabWidget,
                               QToolBar,
                               QMessageBox,
                               QFileDialog,
                               QPushButton,
                               QDialog)
from PySide6.QtGui import QAction
from pathlib import Path
from dialogs.settings_dialog import SettingsDialog
from widgets.DataTab import DataTab
import wholebrain.Observables.BOLDFilters as filters
import global_variables as settings


settings.diagonal_right = False
filters.k = 2  # 2nd order butterworth filter
filters.flp = .008  # lowpass frequency of filter
filters.fhi = .08  # highpass
filters.TR = 0.754  # sampling interval

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tab_names = {}

        self.setWindowTitle("fMRI Visualizer")
        self.setMinimumHeight(100)
        self.setMinimumWidth(300)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_data_tab)
        self.tabs.setTabsClosable(True)

        self.setCentralWidget(self.tabs)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")

        open_file_action = QAction("Open file", self)
        open_file_action.triggered.connect(self.open_file)

        transform_file_action = QAction("Transform file", self)
        transform_file_action.triggered.connect(self.open_file)  # TODO: transform file

        file_menu.addAction(open_file_action)
        file_menu.addAction(transform_file_action)

        options_menu = menu.addMenu("&Options")

        modify_options_action = QAction("Configure settings", self)
        modify_options_action.triggered.connect(self.configure_settings)

        options_menu.addAction(modify_options_action)

        # Add Open File Button
        self.open_file_button = QPushButton("Open File", self)
        self.open_file_button.setGeometry(100, 50, 100, 30)
        self.open_file_button.clicked.connect(self.open_file)

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
            self.open_file_button.hide()
            self.adapt_screen_to_tab()

    def adapt_screen_to_tab(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            tab_size = current_tab.sizeHint()
            self.resize(tab_size.width() + 100, tab_size.height() + 200)

    def add_data_tab(self, data, name):
        tab = DataTab(data, name)
        self.tabs.addTab(tab, name)

    def configure_settings(self):
        dialog = SettingsDialog(settings.diagonal_right, filters.k, filters.TR, filters.flp, filters.fhi)
        if dialog.exec() == QDialog.Accepted:
            diagonal, k, TR, flp, fhi = dialog.get_settings()
            settings.diagonal_right = diagonal
            filters.k = k
            filters.TR = TR
            filters.flp = flp
            filters.fhi = fhi
            for i in range(self.tabs.count()):
                self.tabs.widget(i).update_dialogs()


    def close_data_tab(self, index):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Alert!")
        dlg.setText("Closing this tab will make you lose your work and its corresponding dialogs. Continue?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        if button == QMessageBox.Yes:
            self.tabs.widget(index).before_close()
            self.tabs.removeTab(index)
            if self.tabs.count() == 0:
                self.open_file_button.show()

    def closeEvent(self, event):
        if self.tabs.count() != 0:
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure to quit? All tabs will close, no progress will be saved.",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                while self.tabs.count() > 0:
                    self.tabs.widget(0).before_close()
                    self.tabs.removeTab(0)
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
