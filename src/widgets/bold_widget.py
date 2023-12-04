import numpy as np
from pyqtgraph import PlotWidget


class BOLD(PlotWidget):
    def __init__(self, data):
        super(BOLD, self).__init__()
        self.setAutoFillBackground(True)
        self.data = data
        self.min_y = np.min(data)
        self.max_y = np.max(data)

        self.window_plots = []

        self.x = range(0, data.shape[0])

        n = data.shape[1]
        self.plots = []
        for i in range(0, n):
            self.plots.append(self.plot(self.x, np.squeeze(data[:, i]), pen=(i,n)))

    def plot_window(self, x, w):
        for p in self.window_plots:
            self.removeItem(p)

        self.w = w

        self.window_plots.clear()
        self.window_plots.append(self.plot([x, x], [self.min_y, self.max_y]))
        self.window_plots.append(self.plot([x-w, x-w], [self.min_y, self.max_y]))
        self.window_plots.append(self.plot([x+w, x+w], [self.min_y, self.max_y]))

    def set_ylim(self, min, max):
        self.min_y = min
        self.max_y = max

        self.setYRange(self.min_y, self.max_y)

        for p in self.plots:
            self.removeItem(p)
        self.plots.clear()

        n = self.data.shape[1]
        for i in range(0, n):
            self.plots.append(self.plot(self.x, np.squeeze(self.data[:, i]), pen=(i,n)))
