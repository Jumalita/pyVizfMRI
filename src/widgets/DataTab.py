from PySide6.QtWidgets import (QWidget,
                               QVBoxLayout,
                               QHBoxLayout,
                               QPushButton)
from widgets.series.MultipleLineChart import MultipleLineChart
from widgets.series.RangeControlWidget import RangeControlWidget
from widgets.Dialog import BaseDialog


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
        self.editing = not self.editing
        if self.editing:
            self.range_control_widget.relocate_range()
            self.chart.change_mode(True)
            self.show_edit_layout()
        else:
            self.update_dialogs()
            self.chart.change_mode(False)
            self.show_control_layout()

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
        self.dialog_sw = BaseDialog(self.chart, "sw")
        self.dialog_sw.setWindowTitle("SW " + self.name)
        self.dialog_sw.show()

    def phase(self):
        self.dialog_phase = BaseDialog(self.chart, "phase")
        self.dialog_phase.setWindowTitle("Phase " + self.name)
        self.dialog_phase.show()

    def fc(self):
        self.dialog_fc = BaseDialog(self.chart, "fc")
        self.dialog_fc.setWindowTitle("FC " + self.name)
        self.dialog_fc.show()

    def gbc(self):
        self.dialog_gbc = BaseDialog(self.chart, "vector_heatmap")
        self.dialog_gbc.setWindowTitle("GCB " + self.name)
        self.dialog_gbc.show()

    def gbc3D(self):
        self.dialog_gbc3D = BaseDialog(self.chart, "3d_brain")
        self.dialog_gbc3D.setWindowTitle("3D Brain " + self.name)
        self.dialog_gbc3D.show()

    def update_dialogs(self):
        if self.dialog_fc:
            self.dialog_fc.update()
        if self.dialog_gbc:
            self.dialog_gbc.update()
        if self.dialog_gbc3D:
            self.dialog_gbc3D.update()
        if self.dialog_sw:
            self.dialog_sw.update()
        if self.dialog_phase:
            self.dialog_phase.update()

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