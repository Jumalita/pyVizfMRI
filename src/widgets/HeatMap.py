import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout


class HeatMap(QWidget):
    def __init__(self, data):
        super().__init__()

        glw = pg.GraphicsLayoutWidget()
        self.img = pg.ImageItem(image=data)  # create monochrome image from demonstration data
        pl = glw.addPlot()
        pl.addItem(self.img)
        pl.addColorBar(self.img, colorMap='cividis', values=(0, 1), limits=(0, 1))
        pl.setAspectLocked()
        self.layout = QVBoxLayout()
        self.layout.addWidget(glw)
        self.setLayout(self.layout)

    def update_data(self, data) -> None:
        self.img.setImage(data)
        self.update()
