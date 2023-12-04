from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QHBoxLayout, QComboBox, QLabel, QLineEdit


class DefineInterval(QDialog):
    def __init__(self, message, label, min, max):
        super().__init__()

        self.setWindowTitle(message)
        self.layout = QVBoxLayout()
        self.min_max = (min, max)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        choose = QHBoxLayout()

        choose.addWidget(QLabel(label))

        self.min = QLineEdit()
        self.max = QLineEdit()
        self.min.setText(str(min))
        self.max.setText(str(max))
        choose.addWidget(self.min)
        choose.addWidget(QLabel("-"))
        choose.addWidget(self.max)

        self.layout.addLayout(choose)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def accept(self) -> None:
        self.min_max = (float(self.min.text()), float(self.max.text()))
        super().accept()
