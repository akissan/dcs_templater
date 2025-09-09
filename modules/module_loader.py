from dataclasses import dataclass
from os import path, scandir

from modules.config import Config, sg_config_key

input_path = r"Config\Input"

excluded_folders = ["Default", "UiLayer"]


class Module:
    def __init__(self, path: str, name: str):
        self.path = path
        self.name = name

    def get_modifiers(self):
        pass


def get_modules(config: Config):
    scan_path: str = path.join(config.get("PATHS", sg_config_key), input_path)

    modules = [
        (f.path, f.name)
        for f in scandir(scan_path)
        if f.is_dir() and f.name not in excluded_folders
    ]
    assert len(modules) != 0, "0 compatable modules found"

    print("Found modules", [n for _, n in modules])
    return modules


# @dataclass
# class Keybind:
#     mods: frozenset = {}
#     action: str


def get_modifiers(module: tuple(str, str)):

    pass


def load_module(module):
    load_modifiers = {}
    pass
