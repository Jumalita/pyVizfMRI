import matplotlib.pyplot as plt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from seaborn import heatmap
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

    def plot_heatmap(self,data):
        sns = heatmap([data],square=True)
        plt.show()
        self.canvas.draw()