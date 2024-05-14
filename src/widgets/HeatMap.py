import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QWidget, QVBoxLayout

class HeatMap(QWidget):
    def __init__(self, data):
        super().__init__()

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        self.update_data(data)

    def update_data(self, data):
        self.ax.clear()

        if True:
            data = np.fliplr(data)

        sns.heatmap(data, ax=self.ax, cmap='cividis', cbar=True, cbar_kws={'label': 'Values'})

        self.canvas.draw()
        self.update()
