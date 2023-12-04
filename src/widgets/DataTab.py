from PySide6.QtWidgets import (QWidget,
                               QVBoxLayout,
                               QHBoxLayout,
                               QPushButton)
#from wholebrain.Observables import FC
from widgets.series.MultipleLineChart import MultipleLineChart
from widgets.series.RangeControlWidget import RangeControlWidget


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
        self.compute_fc_button = QPushButton("&Compute FC", self)
        self.compute_fc_button.clicked.connect(self.fc)
        self.control_layout.addWidget(self.to_edit_button)
        self.control_layout.addWidget(self.compute_fc_button)

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

    def phase(self):
        print("calculating phase..")

    def fc(self):
        print("calculating fc...")


