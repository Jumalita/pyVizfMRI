import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel
import pyreadr
import pandas as pd
import scipy.io as sio
from src.widgets.Print3DBrain import Print3DBrain
from wholebrain.Observables import (GBC)
from scipy import spatial

import wholebrain.Observables.BOLDFilters as filters

filters.k = 2  # 2nd order butterworth filter
filters.flp = .008  # lowpass frequency of filter
filters.fhi = .08  # highpass
filters.TR = 0.754  # sampling interval

def find_closest_points(reference, target):
    tree = spatial.cKDTree(reference)
    dist, indexes = tree.query(target)
    return indexes

def launch_app(data, crtx):
    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Create a QWidget instance
    widget = Print3DBrain(data, crtx)

    # Set window properties
    widget.setWindowTitle('PyQt Application')
    widget.setGeometry(100, 100, 1500, 1000)  # (x, y, width, height)

    # Show the window
    widget.show()

    # Start the application event loop
    sys.exit(app.exec())


import nibabel as nib
directory = "./3D_brainmap"

def setCortex(coordinates):
    flat_L = nib.load(directory + '/L.flat.32k_fs_LR.surf.gii')
    flat_R = nib.load(directory + '/R.flat.32k_fs_LR.surf.gii')
    model_L = nib.load(directory + '/L.mid.32k_fs_LR.surf.gii')
    model_R = nib.load(directory + '/R.mid.32k_fs_LR.surf.gii')

    cortex = {
        'map_L': find_closest_points(coordinates, model_L.darrays[0].data),
        'map_R': find_closest_points(coordinates, model_R.darrays[0].data),
        'flat_L': flat_L, 'flat_R': flat_R,
        'model_L': model_L, 'model_R': model_R
    }

    print(cortex["map_L"].shape,cortex["map_L"].shape)
    return cortex

import numpy as np
if __name__ == '__main__':
    name = "aal116"
    result = pyreadr.read_r('C:/Users/juma/Downloads/brainGraph-master/brainGraph-master/data/' + name + ".rda")

    df = pd.DataFrame(result[name])
    df = df[df['lobe'] != "Cerebellum"]
    coordinates = df[['x.mni', 'y.mni', 'z.mni']].values.tolist()

    print(len(coordinates))

    data = sio.loadmat('C:/UDG/TFM/Dades/all_SC_FC_TC_76_90_116.mat')['tc_s0004']


    print(data.shape)
    data = data[0:90]
    print(data.shape)

    cortex = setCortex(coordinates)
    data_to_pass = GBC.from_fMRI(data)
    print("to pass:", data_to_pass)
    launch_app(data_to_pass, cortex)