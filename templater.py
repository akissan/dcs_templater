import json

from os import name, scandir, path

from src.load_confiig import get_configs, get_controllers
from src.load_mods import load_mods
from src.load_diff import get_button_map, get_modules, parse_diff_file, subpath
from src.mapper import Mapper
import gettext

template_folder = "Templates"

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(template_folder))

required_locales = ["en", "ru"]
locales = {
    locale: gettext.translation(
        "input", localedir="Templates/locale", languages=[locale]
    ).gettext
    for locale in required_locales
}

if __name__ == "__main__":
    modules = get_modules()
    # template = env.get_template("base_template.jinja2")
    template = env.get_template("main.jinja2")

    with open("src/icon_map.json") as cm:
        character_map = json.load(cm)

    for module_path, module_name in modules:
        (mod_palette, mod_binds) = load_mods(module_path)
        controllers = get_controllers(path.join(module_path, subpath))
        configs = get_configs(template_folder)
        data = {}

        for locale, translate in locales.items():
            mapper = Mapper(locale)
            for controller_name, diff_path in controllers:
                if controller_name in configs.keys():

                    with open(configs[controller_name], "r") as f:
                        config = json.load(f)

                    diff = parse_diff_file(diff_path)
                    button_map = get_button_map(diff, translate)
                    if controller_name in mod_binds:
                        button_map.update(mod_binds[controller_name])

                    remapped_config = mapper.remap(button_map, config)

                    data[controller_name] = remapped_config

            output = template.render(
                aircraft_name=module_name,
                data=data,
                cdm=character_map,
                mod_palette=mod_palette,
                locale=locale,
            )

            with open(
                path.join(
                    template_folder,
                    "renders",
                    f"{module_name}_{locale}.html",
                ),
                "w",
            ) as f:
                print(output, file=f)
