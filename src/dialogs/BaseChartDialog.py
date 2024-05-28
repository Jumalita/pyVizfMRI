from factory.ChartFactory import ChartFactory
from PySide6.QtWidgets import (QVBoxLayout, QFileDialog, QPushButton,
                               QDialog, QLabel, QWidget)

class BaseChartDialog(QDialog):
    def __init__(self, chart, chart_type):
        super().__init__()
        self.layout = QVBoxLayout()

        self.save_button = QPushButton("Save as PNG")
        self.save_button.clicked.connect(self.save_chart)
        self.layout.addWidget(self.save_button)

        self.chart = chart
        self.chart_type = chart_type
        self.default_brain_mapping_config = None
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
                chart = ChartFactory.create_gbc_3d_brain(self.chart,self.default_brain_mapping_config)
                self.default_brain_mapping_config = chart.returnConfig()
                return chart
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

    def getConfig(self):
        return self.default_brain_mapping_config
