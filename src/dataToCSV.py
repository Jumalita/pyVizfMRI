import os
import numpy as np
import csv
import json
import xml.etree.ElementTree as ET
import pandas as pd
import nibabel as nib
import scipy.io as sio
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QInputDialog

class FileConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Converter")
        self.setGeometry(100, 100, 400, 200)

        self.button = QPushButton("Choose File", self)
        self.button.setGeometry(150, 70, 100, 30)
        self.button.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose File", "", "All Files (*)", options=options)
        if file_name:
            self.convert_to_csv(file_name)

    def json_to_csv(self, input_file, output_file):
        with open(input_file, 'r') as f:
            data = json.load(f)
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def xml_to_csv(self, input_file, output_file):
        tree = ET.parse(input_file)
        root = tree.getroot()
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([child.tag for child in root[0]])
            for elem in root:
                writer.writerow([elem.find(child.tag).text for child in elem])

    def excel_to_csv(self, input_file, output_file):
        df = pd.read_excel(input_file)
        df.to_csv(output_file, index=False)

    def mat_to_csv(self, input_file, output_file):
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

    def nifti_to_csv(self, input_file, output_file):
        img = nib.load(input_file)
        data = img.get_fdata()
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)

    def numpy_to_csv(self, input_file, output_file):
        data = np.load(input_file)
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)

    def txt_to_csv(self, input_file, output_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()
        lines = [line.strip().split() for line in lines]
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(lines)

    def convert_to_csv(self, input_file):
        file_ext = input_file.split('.')[-1].lower()
        output_folder = QFileDialog.getExistingDirectory(self, "Select Directory to Save File", os.path.expanduser('~'))
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + '.csv')
        try:
            if file_ext == 'json':
                self.json_to_csv(input_file, output_file)
            elif file_ext == 'xml':
                self.xml_to_csv(input_file, output_file)
            elif file_ext in ['xls', 'xlsx']:
                self.excel_to_csv(input_file, output_file)
            elif file_ext == 'mat':
                self.mat_to_csv(input_file, output_file)
            elif file_ext == 'nii':
                self.nifti_to_csv(input_file, output_file)
            elif file_ext == 'npy':
                self.numpy_to_csv(input_file, output_file)
            elif file_ext == 'txt':
                self.txt_to_csv(input_file, output_file)
            # Feel free to add more
            else:
                QMessageBox.warning(self, "Unsupported file type", "Unsupported file type")

            if os.path.exists(output_file):
                QMessageBox.information(self, "Success", f"File saved successfully at: {output_file}")
            else:
                QMessageBox.warning(self, "Error", f"Failed to save the file at: {output_file}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error converting file: {str(e)}")


def main():
    app = QApplication([])
    window = FileConverter()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()

