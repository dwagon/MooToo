""" Configuration of the game"""

import json


class Config:
    def __init__(self, filename: str):
        with open(filename) as infh:
            self.data = json.load(infh)

    def __getitem__(self, item):
        return self.data[item]
