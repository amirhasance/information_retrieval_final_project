import os
import pickle
from typing import Any


class Utils:
    @staticmethod
    def save_object_to_file(obj: Any, file_name: str):
        file_path = '/home/amir/Desktop/Projects/IR_Pro/back_up_files/' + file_name
        with open(file_path, 'wb') as file_:
            pickle.dump(obj, file_)

    @staticmethod
    def load_object_from_file(file_name: str) -> Any:
        file_path = '/home/amir/Desktop/Projects/IR_Pro/back_up_files/' + file_name
        with open(file_path, 'rb') as file_:
            data = pickle.load(file_)
        return data

    @staticmethod
    def convert_str_to_int_value(str_: str):
        val = ''
        for char in str_:
            val += str(ord(char))
        return int(val)

