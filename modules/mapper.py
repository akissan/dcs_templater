import json
from os import path
from typing import DefaultDict

map_config_folder = path.join(path.dirname(__file__), "mapper_configs")
map_config_bckpath = path.join(map_config_folder, "en.json")


vaxis = set(["up", "down"])
haxis = set(["left", "right"])
hat = vaxis.union(haxis)
axes = set(["axis_x", "axis_y"])


def clear_axis_direction(element_functions: dict[str, str]):
    mods = set()
    for val in element_functions.values():
        mods.update(val.keys())

    grouped_by_mod = {mod: DefaultDict(list) for mod in mods}

    for direction, functions in element_functions.items():
        for mod, action in functions.items():
            grouped_by_mod[mod][action].append(direction)

    cleaned_functions = DefaultDict(dict)

    for mod, actions in grouped_by_mod.items():
        for action, directions in actions.items():

            dirs = set(directions)
            if dirs == hat:
                cleaned_functions["hat"][mod] = action
            elif dirs == axes:
                cleaned_functions["axes"][mod] = action
            elif dirs == vaxis:
                cleaned_functions["axis_y"][mod] = action
            elif dirs == haxis:
                cleaned_functions["axis_x"][mod] = action
            else:
                for dir in directions:
                    cleaned_functions[dir][mod] = action

    for dir in cleaned_functions:
        cleaned_functions[dir] = sort_default(dict(cleaned_functions[dir]))

    return dict(cleaned_functions)


def sort_default(key_functions: dict):
    if "default" in key_functions:
        key_functions = {
            "default": key_functions.pop("default"),
            **key_functions,
        }
    return key_functions


class Mapper:
    def __init__(self, locale):
        map_config_locpath = path.join(map_config_folder, f"{locale}.json")
        map_config_path = map_config_bckpath
        if path.isfile(map_config_locpath):
            map_config_path = map_config_locpath

        with open(path.join(map_config_path), encoding="utf-8") as mc:
            self.map_config = json.load(mc)
            print(self.map_config)

    def clear_key_function(self, direction: str, key_function: str):

        for wtf, edwtf in self.map_config["wtf"].items():
            key_function = key_function.replace(wtf, edwtf).strip()

        key_function = key_function.strip()

        universal = self.map_config["exclude"]["universal"]
        for s in universal:
            key_function = key_function.removeprefix(s + " ").removesuffix(" " + s)

        key_function = key_function.strip(" -/,")

        direction_map = self.map_config["exclude"]["direction_map"]
        if direction in direction_map:
            for s in direction_map[direction]:
                key_function = key_function.removeprefix(s + " ").removesuffix(" " + s)

        key_function = key_function.strip(" -/,")

        return key_function

    def remap(self, button_map: dict[str, dict[str, str]], template_config):
        final_config = {}
        for section, control_elements in template_config.items():
            final_config[section] = {}

            for control_element, control_data in control_elements.items():
                element_functions = {}

                for control_direction, button in control_data.items():
                    if control_direction == "meta":
                        continue

                    key = str(button).lower()

                    key_functions = button_map.get(key)

                    if not key_functions:
                        continue

                    key_functions = {
                        mod: self.clear_key_function(control_direction, kf)
                        for mod, kf in key_functions.items()
                    }

                    element_functions[control_direction] = sort_default(key_functions)

                if len(element_functions) > 0:
                    element_functions = clear_axis_direction(element_functions)
                    element_functions["meta"] = control_data.get("meta")
                    final_config[section][control_element] = element_functions

        return final_config
