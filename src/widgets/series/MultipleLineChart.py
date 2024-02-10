from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtGui import QPainter, QPen
import numpy as np

from utils import hash_to_color, draw_vertical_line


class MultipleLineChart:
    def __init__(self, data):
        self.data = data
        self.series_list = []

        self.y_range = {}
        self.y_range['min'] = min(x for xs in data for x in xs)
        self.y_range['max'] = max(x for xs in data for x in xs)

        self.chart = QChart()
        self.changeRangeLineMin = draw_vertical_line(0, self.y_range['min'], self.y_range['max'])
        self.changeRangeLineMax = draw_vertical_line(data.shape[0]-1, self.y_range['min'], self.y_range['max'])

        self.range = range(0, data.shape[0])

        self.calculate_series()

        self.chart.legend().hide()
        self.chart.createDefaultAxes()

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

    def calculate_series(self):
        pen = QPen()
        pen.setWidth(0.25)
        self.series_list = []
        self.chart.removeAllSeries()
        n_signals = range(0, self.data.shape[1])
        for i, s in enumerate(n_signals):
            self.series_list.append(QLineSeries())
            pen.setColor(hash_to_color(i))
            self.series_list[s].setPen(pen)
            for t in self.range:
                self.series_list[s].append(t, self.data[t, s])
            self.chart.addSeries(self.series_list[s])

    def chart_view(self):
        return self._chart_view

    def get_range(self, absolute_range):
        if absolute_range:
            return 0, self.data.shape[0]-1
        else:
            return min(self.range), max(self.range)

    def get_data(self):
        return self.data

    def change_range(self, new_range):
        self.range = new_range
        self.calculate_series()

    def move_vertical_line(self, x_min, x_max):
        self.chart.removeAllSeries()

        self.calculate_series()
        self.changeRangeLineMax = draw_vertical_line(x_max, self.y_range['min'], self.y_range['max'])
        self.changeRangeLineMin = draw_vertical_line(x_min, self.y_range['min'], self.y_range['max'])
        self.chart.addSeries(self.changeRangeLineMin)
        self.chart.addSeries(self.changeRangeLineMax)

        self.chart.legend().hide()
        self.chart.createDefaultAxes()

    def change_mode(self, edit):
        if edit:
            vertical_line_x_min = min(self.range)
            vertical_line_x_max = max(self.range)
            self.range = range(0, self.data.shape[0])
            self.move_vertical_line(vertical_line_x_min, vertical_line_x_max)
        else:
            self.calculate_series()
            self.chart.legend().hide()
            self.chart.createDefaultAxes()
