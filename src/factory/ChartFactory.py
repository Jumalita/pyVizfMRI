from src.widgets.HeatMap import HeatMap
from dialogs.sw_params_chooser_dialog import SWParamsDialog
from src.widgets.Print3DBrain import Print3DBrain
from src.widgets.Histogram import VectorHeatmap
from wholebrain.Observables import (FC, phFCD, swFCD, GBC)

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