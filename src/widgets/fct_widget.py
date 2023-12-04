import numpy as np
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from src.widgets.slider_value import SliderValue
from src.widgets.heatmap_widget import HeatMap


class FCtHeatMap(QWidget):
    def __init__(self, data, plot_window):
        super().__init__()

        self.setWindowTitle("Functional connectivity")

        self.data = data
        self.plot_window = plot_window
        self.tmax = data.shape[1]
        self.ws = 3
        d = int(np.floor(self.ws / 2))
        self.time = d

        self.layout = QHBoxLayout()
        self.hm = HeatMap(self.compute_window())
        self.layout.addWidget(self.hm, stretch=10)

        sliders = QVBoxLayout()
        self.slider_ws = SliderValue("Window size:", self.ws, self.tmax, 2, self.update_hm)
        self.slider_t = SliderValue("Time:", d, self.tmax-d, 1, self.update_hm)
        sliders.addWidget(self.slider_ws)
        sliders.addWidget(self.slider_t)

        self.layout.addLayout(sliders, stretch=2)
        self.setLayout(self.layout)

    def update_hm(self):
        if self.slider_ws.value == self.ws and self.slider_t.value == self.time:
            return
        window_changed = self.slider_ws.value != self.ws
        self.ws = self.slider_ws.value
        if window_changed:
            d = int(np.floor(self.ws / 2))
            self.time = d
            self.slider_t.setValue(d)
            self.slider_t.setRange(d, self.tmax-d)
        else:
            self.time = self.slider_t.value

        cc = self.compute_window()
        self.hm.update_data(cc)
        self.update()
        self.plot_window(self.time, int(np.floor(self.ws / 2)))

    def compute_window(self):
        d = int(np.floor(self.ws / 2))
        return np.corrcoef(self.data[:, self.time-d:self.time+d+1])
