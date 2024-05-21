from dataConvert.FileConverter import (FileConverter, JSONConverter, XMLConverter, ExcelConverter, MATConverter,
                                       NIFTIConverter, NumpyConverter, TXTConverter)
from PySide6.QtWidgets import (QInputDialog)
import importlib.util
import os

PLUGIN_DIR = os.path.join(os.path.expanduser('~'), 'pyVizfMRI\\file_converter_plugins')


class ConverterManager:
    def __init__(self):
        self.system_converters = {
            'json': JSONConverter(),
            'xml': XMLConverter(),
            'xls': ExcelConverter(),
            'xlsx': ExcelConverter(),
            'mat': MATConverter(),
            'nii': NIFTIConverter(),
            'npy': NumpyConverter(),
            'txt': TXTConverter()
        }
        self.user_converters = {}
        self.load_plugins()

    def load_plugins(self):
        if os.path.exists(PLUGIN_DIR):
            self.user_converters = {}
            for filename in os.listdir(PLUGIN_DIR):
                if filename.endswith('.py'):
                    plugin_path = os.path.join(PLUGIN_DIR, filename)
                    spec = importlib.util.spec_from_file_location(filename[:-3], plugin_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for name in dir(module):
                        obj = getattr(module, name)
                        if isinstance(obj, type) and issubclass(obj, FileConverter) and obj is not FileConverter:
                            self.user_converters[obj.__name__.lower()] = obj()

    def get_user_converters(self):
        return self.user_converters

    def get_system_converters(self):
        return self.system_converters

    def get_converter(self):
        concatenated_keys = list(self.system_converters.keys()) + list(self.user_converters.keys())
        key, _ = QInputDialog.getItem(None, "Select Key", "Select the key:", concatenated_keys, 0, False)
        if key in self.system_converters.keys():
            return self.system_converters[key]
        else:
            return self.user_converters[key]
