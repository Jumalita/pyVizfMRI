from PySide6.QtWidgets import (QWidget,
                               QVBoxLayout,
                               QHBoxLayout,
                               QPushButton,
                               QDialog)
from wholebrain.Observables import (FC, phFCD, swFCD)
from widgets.series.MultipleLineChart import MultipleLineChart
from widgets.series.RangeControlWidget import RangeControlWidget
from src.widgets.HeatMap import HeatMap
import numpy as np

import wholebrain.Observables.BOLDFilters as filters

filters.k = 2  # 2nd order butterworth filter
filters.flp = .008  # lowpass frequency of filter
filters.fhi = .08  # highpass
filters.TR = 0.754  # sampling interval

class DataTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.editing = False

        self.chart = MultipleLineChart(data)
        self.range_control_widget = RangeControlWidget(self.chart, self.change_layout)

        # Edit layout
        self.edit_layout = QHBoxLayout()
        self.edit_layout.addWidget(self.range_control_widget)

        # Control layout
        self.control_layout = QHBoxLayout()
        self.to_edit_button = QPushButton("&Edit Chart", self)
        self.to_edit_button.clicked.connect(self.change_layout)
        self.control_layout.addWidget(self.to_edit_button)

        self.compute_fc_button = QPushButton("&Compute FC", self)
        self.compute_fc_button.clicked.connect(self.fc)
        self.control_layout.addWidget(self.compute_fc_button)

        self.compute_phase_button = QPushButton("&Compute Phase", self)
        self.compute_phase_button.clicked.connect(self.phase)
        self.control_layout.addWidget(self.compute_phase_button)

        self.compute_sw_button = QPushButton("&Compute SW", self)
        self.compute_sw_button.clicked.connect(self.sw)
        self.control_layout.addWidget(self.compute_sw_button)

        # Plot layout
        self.plot_layout = QHBoxLayout()
        self.plot_layout.addWidget(self.chart.chart_view())

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.plot_layout)
        self.main_layout.addLayout(self.control_layout)
        self.main_layout.addLayout(self.edit_layout)
        self.show_control_layout()

        self.setLayout(self.main_layout)

    def change_layout(self):
        # Toggle between control and edit layouts when the button is clicked
        if self.editing:
            self.range_control_widget.relocate_range()
            self.chart.change_mode(True)
            self.show_edit_layout()
        else:
            self.chart.change_mode(False)
            self.show_control_layout()

        self.editing = not self.editing

    def show_control_layout(self):
        self.range_control_widget.hide()
        self.to_edit_button.show()
        self.compute_fc_button.show()
        self.control_layout.activate()
        self.edit_layout.invalidate()

    def show_edit_layout(self):
        self.range_control_widget.show()
        self.to_edit_button.hide()
        self.compute_fc_button.hide()
        self.control_layout.invalidate()
        self.edit_layout.activate()

    def sw(self):
        print("calculating sw...")
        r_min, r_max = self.chart.get_range(False)
        m = swFCD.from_fMRI(self.data[r_min:r_max].T)
        dlg = FCHeatMap(swFCD.buildFullMatrix(m))
        dlg.exec()

    def phase(self):
        print("calculating phase..")
        r_min, r_max = self.chart.get_range(False)
        m = phFCD.from_fMRI(self.data[r_min:r_max].T)
        dlg = FCHeatMap(phFCD.buildFullMatrix(m))
        dlg.exec()

    def fc(self):
        print("calculating fc...")
        r_min, r_max = self.chart.get_range(False)
        m = FC.from_fMRI(self.data[r_min:r_max].T)
        dlg = FCHeatMap(m)
        dlg.exec()


class FCHeatMap(QDialog):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle("Functional connectivity")

        self.layout = QVBoxLayout()
        self.layout.addWidget(HeatMap(np.corrcoef(data)))
        self.setLayout(self.layout)