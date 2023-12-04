from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QHBoxLayout, QComboBox


class Choose2Opts(QDialog):
    def __init__(self, message, opts):
        super().__init__()

        self.setWindowTitle(message)
        self.layout = QVBoxLayout()
        self.chosen_values = []

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        choose = QHBoxLayout()

        self.b1 = QComboBox()
        self.b1.addItems(opts)
        choose.addWidget(self.b1)

        self.b2 = QComboBox()
        self.b2.addItems(opts)
        choose.addWidget(self.b2)

        self.layout.addLayout(choose)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def accept(self) -> None:
        self.chosen_values = [self.b1.currentText(), self.b2.currentText()]
        super().accept()
