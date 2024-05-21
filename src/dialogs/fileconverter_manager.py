import os
import shutil
from PySide6.QtWidgets import QFileDialog, QMessageBox, QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QGroupBox
import dataConvert.ConverterManager as ConverterManager


def init_pluggin_folder():
    if not os.path.exists(ConverterManager.PLUGIN_DIR):
        os.makedirs(ConverterManager.PLUGIN_DIR)


class FileConverterManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Converter Manager")
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout(self)

        self.system_converters_group = QGroupBox("System Converters")
        self.system_converters_layout = QVBoxLayout()
        self.system_converter_list = QListWidget()
        self.system_converters_layout.addWidget(self.system_converter_list)
        self.system_converters_group.setLayout(self.system_converters_layout)

        self.user_converters_group = QGroupBox("User Plugins")
        self.user_converters_layout = QVBoxLayout()
        self.user_converters_list = QListWidget()
        self.user_converters_layout.addWidget(self.user_converters_list)
        self.user_converters_group.setLayout(self.user_converters_layout)

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Plugin", self)
        self.remove_button = QPushButton("Remove Plugin", self)
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.remove_button)

        self.user_converters_layout.addLayout(self.button_layout)
        self.layout.addWidget(self.system_converters_group)
        self.layout.addWidget(self.user_converters_group)

        self.manager = ConverterManager.ConverterManager()
        self.load_plugins()

        self.add_button.clicked.connect(self.add_plugin)
        self.remove_button.clicked.connect(self.remove_plugin)

    def load_plugins(self):
        init_pluggin_folder()

        self.system_converter_list.clear()
        self.user_converters_list.clear()

        for key in self.manager.get_system_converters().keys():
            self.system_converter_list.addItem(key)

        for key in self.manager.get_user_converters().keys():
            self.user_converters_list.addItem(key)

    def add_plugin(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Add Plugin", "", "Python Files (*.py)", options=options)
        if file_name:
            dest = os.path.join(ConverterManager.PLUGIN_DIR, os.path.basename(file_name))
            if not os.path.exists(dest):
                shutil.copy(file_name, dest)
                self.manager.load_plugins()
                self.load_plugins()
            else:
                QMessageBox.warning(self, "Plugin Exists", "Plugin with the same name already exists.")

    def remove_plugin(self):
        selected_item = self.user_converters_list.currentItem()
        if selected_item:
            plugin_name = selected_item.text()
            plugin_path = os.path.join(ConverterManager.PLUGIN_DIR, f"{plugin_name}.py")
            if os.path.exists(plugin_path):
                os.remove(plugin_path)
                self.manager.load_plugins()
                self.load_plugins()