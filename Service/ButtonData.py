from dataclasses import dataclass
from typing import Type
from typing_extensions import Self
from json import dumps, loads


@dataclass
class Data:
    type: str
    extra_data: str
    def __getitem__(self, key):
        return self.extra_data[key]


@dataclass
class ButtonData:

    def __init__(self, label: str, type: str, disabled: bool = True, extra_data = None):
        self.label = label
        self.type = type
        self.disabled = disabled
        self.extra_data = extra_data or {}

    def to_json(self) -> str:
        return dumps({"type":self.type,"extra_data":self.extra_data})

    @classmethod
    def from_json(cls, json_string: str) -> Data:
        return Data(**loads(json_string))
    
    def __getitem__(self, key):
        return self.extra_data[key]

    def __setitem__(self, key, value):
        self.extra_data[key] = value