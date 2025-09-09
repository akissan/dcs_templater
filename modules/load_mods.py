from os import path

from src.load_confiig import get_controller_name
from src.load_diff import clean_bind, parse_diff_file


mod_filename = "modifiers.lua"


def load_mods(module_path):

    default_mod = {"default": "default"}

    mod_filepath = path.join(module_path, mod_filename)
    if path.isfile(mod_filepath):
        mod_file = parse_diff_file(mod_filepath)

        mods = {
            mod: mod_info
            for mod, mod_info in mod_file.items()
            if mod_info["device"] != "Keyboard"
        }

        palette = []
        for i in range(15, 0, -1):
            palette.append(f"mod_{i}")

        mod_palette = {mod: palette.pop() for mod in mods}

        mod_binds = {}
        for mod, mod_info in mods.items():
            device = get_controller_name(mod_info["device"])
            if not device in mod_binds:
                mod_binds[device] = {}

            mod_binds[device][clean_bind(mod_info["key"])] = {mod: f"MOD: {mod}"}

        return ({**default_mod, **mod_palette}, mod_binds)

    return (default_mod, {})
