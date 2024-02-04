from PySide6.QtWidgets import (QWidget,
                               QVBoxLayout,
                               QHBoxLayout,
                               QPushButton,
                               QDialog)
from wholebrain.Observables import (FC, phFCD, swFCD, GBC)
from widgets.series.MultipleLineChart import MultipleLineChart
from widgets.series.RangeControlWidget import RangeControlWidget
from src.widgets.HeatMap import HeatMap
from src.widgets.Print3DBrain import Print3DBrain
from src.widgets.Histogram import VectorHeatmap
import numpy as np

import wholebrain.Observables.BOLDFilters as filters

filters.k = 2  # 2nd order butterworth filter
filters.flp = .008  # lowpass frequency of filter
filters.fhi = .08  # highpass
filters.TR = 0.754  # sampling interval


class DataTab(QWidget):
    def __init__(self, data, name):
        super().__init__()
        self.data = data
        self.name = name
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
        self.dialog_fc = None

        self.compute_phase_button = QPushButton("&Compute Phase", self)
        self.compute_phase_button.clicked.connect(self.phase)
        self.control_layout.addWidget(self.compute_phase_button)
        self.dialog_phase = None

        self.compute_sw_button = QPushButton("&Compute SW", self)
        self.compute_sw_button.clicked.connect(self.sw)
        self.control_layout.addWidget(self.compute_sw_button)
        self.dialog_sw = None

        self.compute_gbc_button = QPushButton("&Compute GBC", self)
        self.compute_gbc_button.clicked.connect(self.gbc)
        self.control_layout.addWidget(self.compute_gbc_button)
        self.dialog_gbc = None

        self.compute_3Dgbc_button = QPushButton("&Compute 3D GBC", self)
        self.compute_3Dgbc_button.clicked.connect(self.gbc3D)
        self.control_layout.addWidget(self.compute_3Dgbc_button)
        self.dialog_gbc3D = None

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
        self.compute_phase_button.show()
        self.compute_sw_button.show()
        self.compute_gbc_button.show()
        self.compute_3Dgbc_button.show()
        self.control_layout.activate()
        self.edit_layout.invalidate()

    def show_edit_layout(self):
        self.range_control_widget.show()
        self.to_edit_button.hide()
        self.compute_fc_button.hide()
        self.compute_phase_button.hide()
        self.compute_sw_button.hide()
        self.compute_gbc_button.hide()
        self.compute_3Dgbc_button.hide()
        self.control_layout.invalidate()
        self.edit_layout.activate()

    def sw(self):
        print("calculating sw...")
        r_min, r_max = self.chart.get_range(False)
        m = swFCD.from_fMRI(self.data[r_min:r_max].T)
        self.dialog_sw = FCHeatMap(swFCD.buildFullMatrix(m))
        self.dialog_sw.setWindowTitle("SW " + self.name)
        self.dialog_sw.show()

    def phase(self):
        print("calculating phase...")
        r_min, r_max = self.chart.get_range(False)
        m = phFCD.from_fMRI(self.data[r_min:r_max].T, applyFilters=False)
        self.dialog_phase = FCHeatMap(phFCD.buildFullMatrix(m))
        self.dialog_phase.setWindowTitle("Phase " + self.name)
        self.dialog_phase.show()

    def fc(self):
        print("calculating fc...")
        r_min, r_max = self.chart.get_range(False)
        m = FC.from_fMRI(self.data[r_min:r_max].T)
        self.dialog_fc = FCHeatMap(m)
        self.dialog_fc.setWindowTitle("FC " + self.name)
        self.dialog_fc.show()

    def gbc(self):
        print("calculating gbc...")
        r_min, r_max = self.chart.get_range(False)
        m = GBC.from_fMRI(self.data[r_min:r_max])
        self.dialog_gbc = FCHeatMap(m, is_vector=True)
        self.dialog_gbc.setWindowTitle("GCB " + self.name)
        self.dialog_gbc.show()

    def gbc3D(self):
        print("calculating 3D gbc...")
        r_min, r_max = self.chart.get_range(False)
        m = GBC.from_fMRI(self.data[:, r_min:r_max])
        self.dialog_gbc3D = FC3D(m)
        self.dialog_gbc3D.setWindowTitle("3D Brain " + self.name)
        self.dialog_gbc3D.show()

    def before_close(self):
        if self.dialog_fc:
            self.dialog_fc.close()
        if self.dialog_gbc:
            self.dialog_gbc.close()
        if self.dialog_gbc3D:
            self.dialog_gbc3D.close()
        if self.dialog_sw:
            self.dialog_sw.close()
        if self.dialog_phase:
            self.dialog_phase.close()


class FCHeatMap(QDialog):
    def __init__(self, data, is_vector=False):
        super().__init__()

        self.layout = QVBoxLayout()
        if is_vector:
            self.layout.addWidget(VectorHeatmap(data))
        else:
            self.layout.addWidget(HeatMap(np.corrcoef(data)))
        self.setLayout(self.layout)


class FC3D(QDialog):
    def __init__(self, data):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.addWidget(Print3DBrain(data))
        self.setLayout(self.layout)
