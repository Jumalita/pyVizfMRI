from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QMessageBox
from scipy import spatial
from wholebrain.Utils.plot3DBrain_Utils import setUpGlasser360, multiview5
from matplotlib import cm, pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from wholebrain.Utils.plot3DBrain import *
import pyreadr
import pandas as pd
import re

directory = "./3D_brainmap"


def find_closest_points(reference, target):
    tree = spatial.cKDTree(reference)
    dist, indexes = tree.query(target)
    return indexes


def set_up_cortex(coordinates):
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

    return cortex


class Print3DBrain(QWidget):
    def __init__(self, data):
        super().__init__()
        self.figure, self.ax = plt.subplots(2, 3, figsize=(15, 10))
        self.canvas = FigureCanvas(self.figure)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.plot_3d_brain(data)

    def plot_3d_brain(self, b_data):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Default configuration")
        dlg.setText("You want to use Glasser360? Otherwise you will have to upload a config file.")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec()
        if button == QMessageBox.Yes:
            crtx = setUpGlasser360()
        else:
            filename, _ = QFileDialog.getOpenFileName(
                parent=self,
                caption="Open RDA files...",
                filter="Map files (*.rda)"
            )
            result = pyreadr.read_r(filename)
            pattern = r"\/([^\/]+)\.rda$"
            name = re.search(pattern, filename).group(1)
            df = pd.DataFrame(result[name])
            df = df[df['lobe'] != "Cerebellum"]
            coords_from_file = df[['x.mni', 'y.mni', 'z.mni']].values.tolist()
            crtx = set_up_cortex(coords_from_file)

        data = {'func_L': b_data, 'func_R': b_data}
        testColors = cm.YlOrBr
        self.plt_brainview(crtx, data, len(b_data), testColors, lightingBias=0.1, mode='flatWire', shadowed=True)
        self.canvas.draw()

    def plt_brainview(self, cortex, data, numRegions, cmap=plt.cm.coolwarm,
               suptitle='', **kwds):
        plotColorView(self.ax[0, 0], cortex, data, numRegions, 'Lh-lateral', cmap=cmap, **kwds)
        plotColorView(self.ax[1, 0], cortex, data, numRegions, 'Lh-medial', cmap=cmap, **kwds)
        plotColorView(self.ax[0, 2], cortex, data, numRegions, 'Rh-lateral', cmap=cmap, **kwds)
        plotColorView(self.ax[1, 2], cortex, data, numRegions, 'Rh-medial', cmap=cmap, **kwds)
        # === L/R-superior
        gs = self.ax[0, 1].get_gridspec()
        # remove the underlying axes
        for ax in self.ax[:, 1]:
            ax.remove()
        axbig = self.figure.add_subplot(gs[:, 1])
        plotColorView(axbig, cortex, data, numRegions, 'L-superior', suptitle=suptitle, cmap=cmap, **kwds)
        plotColorView(axbig, cortex, data, numRegions, 'R-superior', suptitle=suptitle, cmap=cmap, **kwds)
        # ============= Adjust the sizes
        plt.subplots_adjust(left=0.0, right=0.8, bottom=0.0, top=1.0, wspace=0, hspace=0)
        # ============= now, let's add a colorbar...
        if 'norm' not in kwds:
            vmin = np.min(data['func_L']) if 'vmin' not in kwds else kwds['vmin']
            vmax = np.max(data['func_L']) if 'vmax' not in kwds else kwds['vmax']
            norm = Normalize(vmin=vmin, vmax=vmax)
        else:
            norm = kwds['norm']
        PCM = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
        cbar_ax = self.figure.add_axes(
            [0.85, 0.15, 0.02, 0.7])  # This parameter is the dimensions [left, bottom, width, height] of the new axes.
        self.figure.colorbar(PCM, cax=cbar_ax)

        plt.show()