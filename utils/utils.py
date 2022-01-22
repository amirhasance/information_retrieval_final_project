import os
import pickle
from typing import Any
from pathlib import Path


class Utils:
    @staticmethod
    def save_object_to_file(obj: Any, file_name: str):
        file = os.path.join(Path(__file__).parent.parent, 'backup_files', file_name)
        with open(file_name, 'wb') as file_:
            pickle.dump(obj, file_)

    @staticmethod
    def load_object_from_file(file_name: str) -> Any:
        file = os.path.join(Path(__file__).parent.parent, 'backup_files', file_name)
        with open(file, 'rb') as file_:
            data = pickle.load(file_)
        return data

    @staticmethod
    def convert_str_to_int_value(str_: str):
        val = ''
        for char in str_:
            val += str(ord(char))
        return int(val)
