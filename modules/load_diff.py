import gettext
from os import scandir, path
from typing import DefaultDict
import lupa


scan_path = "."
subpath = "joystick"

supported_modules = ["A-10C II", "F-16C_50", "FA-18C_hornet", "Mi-24P_pilot"]
# supported_modules = ["A-10C II"]


def parse_diff_file(diff_filepath):
    with open(diff_filepath) as f:
        diff_file = f.read()
    diff_file = diff_file[diff_file.index("{") : diff_file.rindex("}") + 1]
    lua_table = lua.eval(diff_file)
    diff = convert_table_to_dict(lua_table)
    return diff


def clean_bind(bind: str):
    bind = bind.lower()
    if "pov" in bind and "pov_" not in bind:
        bind = bind.replace("pov", "pov_")
    return (
        bind.removeprefix("joy").removeprefix("_").removeprefix("btn").removeprefix("_")
    )


def get_button_map(diff: dict, translate):
    button_map = DefaultDict(dict)
    categories = ["axisDiffs", "keyDiffs"]

    for cat in diff:
        if cat not in categories:
            continue
        for _, bind in diff[cat].items():
            if "added" in bind:
                key_info = bind["added"][1]

                keybind: str = clean_bind(key_info["key"])

                reformers = key_info.get("reformers")
                if not reformers:
                    keymodifier = "default"
                else:
                    keymodifier = key_info["reformers"][1]

                name = bind["name"]
                reverse = reverse_mapping[name] if name in reverse_mapping else name

                button_map[keybind][keymodifier] = translate(reverse)

    button_map = dict(button_map)
    return button_map
