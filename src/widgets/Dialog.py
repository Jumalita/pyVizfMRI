from src.widgets.HeatMap import HeatMap
from src.widgets.sw_params_chooser_dialog import SWParamsDialog
from src.widgets.Print3DBrain import Print3DBrain
from src.widgets.Histogram import VectorHeatmap, Histogram
from wholebrain.Observables import (FC, phFCD, swFCD, GBC)
from PySide6.QtWidgets import (QVBoxLayout, QFileDialog, QPushButton,
                               QDialog, QLabel, QWidget)
import wholebrain.Observables.BOLDFilters as filters

filters.k = 2  # 2nd order butterworth filter
filters.flp = .008  # lowpass frequency of filter
filters.fhi = .08  # highpass
filters.TR = 0.754  # sampling interval


class BaseDialog(QDialog):
    def __init__(self, chart, chart_type):
        super().__init__()
        self.layout = QVBoxLayout()

        self.save_button = QPushButton("Save as PNG")
        self.save_button.clicked.connect(self.save_chart)
        self.layout.addWidget(self.save_button)

        self.chart = chart
        self.chart_type = chart_type
        self.setMinimumHeight(500)
        self.setMinimumWidth(400)
        self.layout.addWidget(self.calculate())

        self.setLayout(self.layout)

    def calculate(self):
        try:
            self.save_button.setDisabled(False)
            if self.chart_type == 'fc':
                return ChartFactory.create_fc_heatmap(self.chart)
            elif self.chart_type == 'phase':
                return ChartFactory.create_phase_heatmap(self.chart)
            elif self.chart_type == 'vector_heatmap':
                return ChartFactory.create_gbc_vector_heatmap(self.chart)
            elif self.chart_type == '3d_brain':
                return ChartFactory.create_gbc_3d_brain(self.chart)
            elif self.chart_type == 'sw':
                return ChartFactory.create_sw_heatmap(self.chart)
        except Exception as e:
            widget = QWidget()
            label = QLabel("Phase cannot be computed: " + str(e))
            layout = QVBoxLayout()
            layout.addWidget(label)
            widget.setLayout(layout)
            self.save_button.setDisabled(True)
            return widget

    def update(self):
        existing_widget = self.layout.itemAt(1).widget()
        new_widget = self.calculate()
        if existing_widget is not None:
            existing_widget.deleteLater()
        self.layout.addWidget(new_widget)

    def save_chart(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Chart", "", "PNG (*.png)")
        if filepath:
            chart_widget = self.layout.itemAt(0).widget()
            if chart_widget:
                pixmap = chart_widget.grab()
                pixmap.save(filepath, "PNG")

class ChartFactory:
    @staticmethod
    def get_chart_data(chart):
        r_min, r_max = chart.get_range(False)
        data = chart.get_data()
        return data[r_min:r_max+1]

    @staticmethod
    def create_heatmap(chart, transformation_function):
        transformed_data = transformation_function(ChartFactory.get_chart_data(chart))
        return HeatMap(transformed_data.T)

    @staticmethod
    def create_fc_heatmap(chart):
        return ChartFactory.create_heatmap(chart, lambda data: FC.from_fMRI(data.T))

    @staticmethod
    def create_sw_heatmap(chart):
        params_dialog = SWParamsDialog(swFCD, ChartFactory.get_chart_data(chart))
        params_dialog.exec()
        return ChartFactory.create_heatmap(chart, lambda data: swFCD.buildFullMatrix(swFCD.from_fMRI(data.T)))

    @staticmethod
    def create_phase_heatmap(chart):
        return ChartFactory.create_heatmap(chart, lambda data: phFCD.buildFullMatrix(phFCD.from_fMRI(data, applyFilters=False)))


    @staticmethod
    def create_gbc_vector_heatmap(chart):
        return VectorHeatmap(GBC.from_fMRI(ChartFactory.get_chart_data(chart)))

    @staticmethod
    def create_gbc_3d_brain(chart):
        return Print3DBrain(GBC.from_fMRI(ChartFactory.get_chart_data(chart)))

