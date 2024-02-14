import pickle
import json
import os


class SaveLoadSystem:
    def __init__(self, file_extension):
        self.file_extension = file_extension

    def save_data(self, name, data):
        with open(str(name) + self.file_extension, "w") as save_file:
            json.dump(data, save_file)

    def load_data(self, name):
        with open(str(name)) as load_file:
            data = json.load(load_file)
        return data
