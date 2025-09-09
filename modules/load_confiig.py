from os import scandir


def get_controller_name(f: str):
    return f.split("{")[0].strip()


def get_controllers(basepath: str):
    controllers = [
        (get_controller_name(f.name), f.path, f.stat().st_mtime)
        for f in scandir(basepath)
    ]

    unique_controllers = {}

    for name, path, mtime in controllers:
        if name not in unique_controllers or mtime > unique_controllers[name][1]:
            unique_controllers[name] = (path, mtime)

    return [(name, data[0]) for name, data in unique_controllers.items()]


def get_configs(template_folder):
    configs = {
        f.name.removesuffix(".json"): f.path
        for f in scandir(template_folder)
        if f.is_file() and f.name.endswith(".json")
    }
    return configs
