import csv
import json
import xml.etree.ElementTree as ET
import pandas as pd
import nibabel as nib
import scipy.io as sio
import numpy as np
from PySide6.QtWidgets import (QInputDialog)
from abc import ABC, abstractmethod


class FileConverter(ABC):
    @abstractmethod
    def convert(self, input_file, output_file):
        pass


class JSONConverter(FileConverter):
    ext = "json"

    def convert(self, input_file, output_file):
        with open(input_file, 'r') as f:
            data = json.load(f)
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


class XMLConverter(FileConverter):
    ext = "xml"

    def convert(self, input_file, output_file):
        tree = ET.parse(input_file)
        root = tree.getroot()
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([child.tag for child in root[0]])
            for elem in root:
                writer.writerow([elem.find(child.tag).text for child in elem])


class ExcelConverter(FileConverter):
    ext = "xlsx"

    def convert(self, input_file, output_file):
        df = pd.read_excel(input_file)
        df.to_csv(output_file, index=False)


class MATConverter(FileConverter):
    ext = "mat"

    def convert(self, input_file, output_file):
        mat_dict = sio.loadmat(input_file)
        keys = list(mat_dict.keys())
        if len(keys) == 1:
            key = keys[0]
        else:
            key, _ = QInputDialog.getItem(None, "Select Key", "Select the key:", keys, 0, False)
        data = mat_dict[key]
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)


class NIFTIConverter(FileConverter):
    ext = "nii"

    def convert(self, input_file, output_file):
        img = nib.load(input_file)
        data = img.get_fdata()
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)


class NumpyConverter(FileConverter):
    ext = "npy"

    def convert(self, input_file, output_file):
        data = np.load(input_file)
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)


class TXTConverter(FileConverter):
    ext = "txt"

    def convert(self, input_file, output_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()
        lines = [line.strip().split() for line in lines]
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(lines)
