from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider


class SliderValue(QWidget):
    def __init__(self, message, min, max, step, func):
        super().__init__()

        self.message = message

        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.slider = QSlider()
        self.slider.setRange(min, max)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setSingleStep(step)
        self.slider.valueChanged.connect(self.updateText)
        self.slider.valueChanged.connect(func)

        self.updateText()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)

        self.setLayout(self.layout)

    @property
    def value(self):
        return self.slider.value()

    def updateText(self):
        value = self.value
        self.label.setText(self.message + f" {value}")

    def setRange(self, min, max):
        self.slider.setRange(min, max)

    def setValue(self, v):
        self.slider.setValue(v)
