from modules.config import Config
from modules.locale_loader import LocaleManager
from modules.module_loader import get_modules

template_folder = "Templates"

from jinja2 import Environment, FileSystemLoader, ModuleLoader

env = Environment(loader=FileSystemLoader(template_folder))


class Templater:
    def __init__(self, config: Config):
        self.config = config

    def generate_templates(self):
        self.config.print_config("Generating Templates for config: ")
        template = env.get_template("main.jinja2")

        module_paths = get_modules(self.config)
        lm = LocaleManager(self.config)

        for module in module_paths:


        # print(raw_modules)
