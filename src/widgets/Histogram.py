import matplotlib.pyplot as plt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from seaborn import heatmap, histplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class VectorHeatmap(QWidget):
    def __init__(self, data):
        super().__init__()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.plot_heatmap(data)

    def plot_heatmap(self, data):
        heatmap([data], square=True)
        plt.show()
        self.canvas.draw()


class Histogram(QWidget):
    def __init__(self, data):
        super().__init__()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.plot_histogram(data)

    def plot_histogram(self, data):
        histplot(data, ax=self.ax)
        self.ax.set_title("Histogram")
        self.canvas.draw()
