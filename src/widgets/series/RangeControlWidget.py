from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from superqt import QLabeledRangeSlider


class RangeControlWidget(QWidget):
    def __init__(self, multiple_line_chart, on_cancel_function):
        super(RangeControlWidget, self).__init__()

        self.multiple_line_chart = multiple_line_chart
        self.range_slider = QLabeledRangeSlider(Qt.Horizontal)
        self.accept_button = QPushButton("&Accept", self)
        self.accept_button.clicked.connect(self.on_accept)
        self.cancel_button = QPushButton("&Cancel", self)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.on_cancel_function = on_cancel_function

        abs_min, abs_max = multiple_line_chart.get_range(True)
        loc_min, loc_max = multiple_line_chart.get_range(False)
        self.range_slider.setRange(abs_min, abs_max)
        self.range_slider.setValue((loc_min, loc_max))

        self.label = QLabel("Range:")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.range_slider)
        self.layout.addWidget(self.accept_button)
        self.layout.addWidget(self.cancel_button)

        self.range_slider.valueChanged.connect(lambda e: self.change_value(e))

    def relocate_range(self):
        loc_min, loc_max = self.multiple_line_chart.get_range(False)
        self.range_slider.setValue((loc_min, loc_max))

    def change_value(self, range_tuple):
        self.multiple_line_chart.move_vertical_line(range_tuple[0], range_tuple[1])

    def on_accept(self):
        self.multiple_line_chart.change_range(range(self.range_slider.value()[0], self.range_slider.value()[1]+1))
        self.on_cancel_function()

    def on_cancel(self):
        self.on_cancel_function()
