import os
import shutil
from PySide6.QtWidgets import QFileDialog, QMessageBox, QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QGroupBox
import brain_map.BrainMapFilesManager as manager


def init_mapping_folder():
    if not os.path.exists(manager.MAPPING_FILES_DIR):
        os.makedirs(manager.MAPPING_FILES_DIR)


class BrainMapFilesManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("3D Brain Map Files Manager")
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout(self)

        self.system_file_mapping_group = QGroupBox("System 3D Brain Map Files")
        self.system_file_mapping_layout = QVBoxLayout()
        self.system_file_mapping_list = QListWidget()
        self.system_file_mapping_layout.addWidget(self.system_file_mapping_list)
        self.system_file_mapping_group.setLayout(self.system_file_mapping_layout)

        self.user_file_mapping_group = QGroupBox("User 3D Brain Map Files")
        self.user_file_mapping_layout = QVBoxLayout()
        self.user_file_mapping_list = QListWidget()
        self.user_file_mapping_layout.addWidget(self.user_file_mapping_list)
        self.user_file_mapping_group.setLayout(self.user_file_mapping_layout)

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add File", self)
        self.remove_button = QPushButton("Remove File", self)
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.remove_button)

        self.user_file_mapping_layout.addLayout(self.button_layout)
        self.layout.addWidget(self.system_file_mapping_group)
        self.layout.addWidget(self.user_file_mapping_group)

        self.manager = manager.BrainMapManager()
        self.load_plugins()

        self.add_button.clicked.connect(self.add_file)
        self.remove_button.clicked.connect(self.remove_file)

    def load_plugins(self):
        init_mapping_folder()

        self.system_file_mapping_list.clear()
        self.user_file_mapping_list.clear()

        for key in self.manager.get_system_files().keys():
            self.system_file_mapping_list.addItem(key)

        for key in self.manager.get_user_files().keys():
            self.user_file_mapping_list.addItem(key)

    def add_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Add File", "", "Python Files (*.rda)", options=options)
        if file_name:
            dest = os.path.join(manager.MAPPING_FILES_DIR, os.path.basename(file_name))
            if not os.path.exists(dest):
                shutil.copy(file_name, dest)
                self.manager.load_plugins()
                self.load_plugins()
            else:
                QMessageBox.warning(self, "File Exists", "File with the same name already exists.")

    def remove_file(self):
        selected_item = self.user_file_mapping_list.currentItem()
        if selected_item:
            plugin_name = selected_item.text()
            plugin_path = os.path.join(manager.MAPPING_FILES_DIR, f"{plugin_name}")
            if os.path.exists(plugin_path):
                os.remove(plugin_path)
                self.manager.load_plugins()
                self.load_plugins()