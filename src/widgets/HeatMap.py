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
        # Clear previous heatmap
        self.ax.clear()

        # Create a heatmap using seaborn
        sns.heatmap(data, ax=self.ax, cmap='cividis', cbar=True, cbar_kws={'label': 'Values'})

        # Redraw canvas
        self.canvas.draw()
        self.update()
