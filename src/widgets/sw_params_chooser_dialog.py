from PySide6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QSpinBox, QPushButton
from widgets.series.MultipleLineChart import MultipleLineChart

class SWParamsDialog(QDialog):
    def __init__(self, swFCD, chart_data, parent=None):
        super().__init__(parent)

        self.setMinimumHeight(400)
        self.setMinimumWidth(1000)

        self.chart = MultipleLineChart(chart_data)
        self.swFCD = swFCD

        self.setWindowTitle("Sliding Window Settings")

        # Settings layout
        self.settings_layout = QVBoxLayout()
        self.settings_layout.addStretch()

        self.window_size_label = QLabel("Window Size:")
        self.window_size_input = QSpinBox()
        self.window_size_input.setMinimum(1)
        self.window_size_input.setMaximum(self.chart.get_range(True)[1])
        self.window_size_input.setValue(swFCD.windowSize)
        self.settings_layout.addWidget(self.window_size_label)
        self.settings_layout.addWidget(self.window_size_input)
        self.window_size_input.valueChanged.connect(self.update_chart)


        self.window_step_label = QLabel("Window Step:")
        self.window_step_input = QSpinBox()
        self.window_step_input.setMinimum(1)
        self.window_step_input.setMaximum(self.chart.get_range(True)[1])
        self.window_step_input.setValue(swFCD.windowStep)
        self.settings_layout.addWidget(self.window_step_label)
        self.settings_layout.addWidget(self.window_step_input)
        self.window_step_input.valueChanged.connect(self.update_chart)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.on_ok)
        self.settings_layout.addWidget(self.ok_button)


        self.settings_layout.addStretch()

        # Plot layout
        self.plot_layout = QHBoxLayout()
        self.plot_layout.addWidget(self.chart.chart_view())

        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addLayout(self.plot_layout)
        self.main_layout.addLayout(self.settings_layout)

        self.update_chart()

    def update_chart(self):
        self.chart.represent_sw(self.window_size_input.value(), self.window_step_input.value())

    def on_ok(self):
        self.swFCD.windowSize = self.window_size_input.value()
        self.swFCD.windowStep = self.window_step_input.value()
        self.accept()
