from PySide6.QtWidgets import (QInputDialog)
import os

MAPPING_FILES_DIR = os.path.join(os.path.expanduser('~'), 'pyVizfMRI\\brain_mappings_files')
SYSTEM_MAPPING_FILES_DIR = "./mappings"

class BrainMapManager:
    def __init__(self):
        self.system_mappings = {}
        self.user_mappings = {}
        self.load_plugins()

    def load_plugins(self):
        if os.path.exists(SYSTEM_MAPPING_FILES_DIR):
            self.system_mappings = {}
            for filename in os.listdir(SYSTEM_MAPPING_FILES_DIR):
                if filename.endswith('.rda'):
                    file_path = os.path.join(SYSTEM_MAPPING_FILES_DIR, filename)
                    self.system_mappings[filename] = file_path

        if os.path.exists(MAPPING_FILES_DIR):
            self.user_mappings = {}
            for filename in os.listdir(MAPPING_FILES_DIR):
                if filename.endswith('.rda'):
                    file_path = os.path.join(MAPPING_FILES_DIR, filename)
                    self.user_mappings[filename] = file_path
    def get_user_files(self):
        return self.user_mappings

    def get_system_files(self):
        return self.system_mappings

    def get_converter_path(self):
        concatenated_keys = list(self.user_mappings.keys()) + list(self.system_mappings.keys())
        key, _ = QInputDialog.getItem(None, "Select Key", "Select the key:", concatenated_keys, 0, False)
        if key in self.user_mappings.keys():
            return self.user_mappings[key]
        else:
            return self.system_mappings[key]
