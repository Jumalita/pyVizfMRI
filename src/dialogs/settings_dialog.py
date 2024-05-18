from PySide6.QtWidgets import QDialog, QVBoxLayout, QRadioButton, QLabel, QSpinBox, QDoubleSpinBox, QDialogButtonBox, QCheckBox


class SettingsDialog(QDialog):
    def __init__(self, diagonal_right, k, TR, flp, fhi, dTrent):
        super().__init__()
        self.k = k
        self.TR = TR
        self.diagonal_right = diagonal_right
        self.flp = flp
        self.fhi = fhi
        self.setWindowTitle("Configure Settings")

        layout = QVBoxLayout()

        # Radio buttons for diagonal
        diagonal_label = QLabel("Diagonal:")
        layout.addWidget(diagonal_label)

        self.left_radio = QRadioButton("Left")
        self.left_radio.setChecked(not diagonal_right)
        self.right_radio = QRadioButton("Right")
        self.right_radio.setChecked(diagonal_right)
        layout.addWidget(self.left_radio)
        layout.addWidget(self.right_radio)

        # Input for k
        k_label = QLabel("k:")
        self.k_input = QSpinBox()
        self.k_input.setMinimum(1)
        self.k_input.setSingleStep(1)
        self.k_input.setMaximum(50)
        self.k_input.setValue(k)
        layout.addWidget(k_label)
        layout.addWidget(self.k_input)

        # Input for TR
        TR_label = QLabel("TR:")
        self.TR_input = QDoubleSpinBox()
        self.TR_input.setDecimals(3)
        self.TR_input.setSingleStep(0.001)
        self.TR_input.setMinimum(0.5)
        self.TR_input.setMaximum(5)
        self.TR_input.setValue(TR)
        self.TR_input.valueChanged.connect(self.tr_change_value)
        layout.addWidget(TR_label)
        layout.addWidget(self.TR_input)

        # Input for flp
        flp_label = QLabel("flp:")
        self.flp_input = QDoubleSpinBox()
        self.flp_input.setDecimals(3)
        self.flp_input.setSingleStep(0.001)
        self.flp_input.setMinimum(0.001)
        self.flp_input.setMaximum(0.1)
        self.flp_input.setValue(flp)
        self.flp_input.valueChanged.connect(self.flp_change_value)
        layout.addWidget(flp_label)
        layout.addWidget(self.flp_input)

        # Input for fli
        fhi_label = QLabel("fli:")
        self.fhi_input = QDoubleSpinBox()
        self.fhi_input.setDecimals(3)
        self.fhi_input.setSingleStep(0.001)
        self.fhi_input.setMinimum(1)
        self.fhi_input.setMaximum(1/2 * 1/TR)
        self.fhi_input.setValue(fhi)
        layout.addWidget(fhi_label)
        layout.addWidget(self.fhi_input)

        #dTrent
        self.dTrent_checkbox = QCheckBox("Apply final Detrend")
        layout.addWidget(self.dTrent_checkbox)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def tr_change_value(self):
        self.fhi_input.setMaximum((1/2)*(1/self.TR_input.value()))

    def flp_change_value(self):
        self.fhi_input.setMinimum(self.flp_input.value())

    def get_settings(self):
        diagonal_right = self.right_radio.isChecked()
        k = int(self.k_input.value())
        TR = float(self.TR_input.value())
        flp = float(self.flp_input.value())
        fhi = float(self.fhi_input.value())
        dTrent = self.dTrent_checkbox.isChecked()
        return diagonal_right, k, TR, flp, fhi, dTrent