from configparser import ConfigParser
import os
from babel import Locale
import babel

sg_config_key = "dcs_savedgames"
dcs_config_key = "dcs_folder"
loc_needed_key = "loc_needed"


class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.load_config()
        self.print_config("Init Config: ")

    def update_tkinker(self, tkinker, key, value):
        if tkinker:
            tkinker.vars.set(key, value)

    def get(self, section: str, key: str, fallback=None, type: str | bool = str):
        if type == str:
            return self.config.get(section, key, fallback=fallback)
        elif type == bool:
            return self.config.getboolean(section, key, fallback=False)

    def get_savedgames_path(self):
        return self.config.get("PATHS", sg_config_key)

    def set_savedgames_path(self, path, tkinker=None, force=False):
        if force or check_savedgames_path(path):
            self.config["PATHS"][sg_config_key] = path
            self.update_tkinker(tkinker, sg_config_key, path)
            self.save_config()

    def get_dcs_path(self):
        return self.config.get("PATHS", dcs_config_key)

    def set_dcs_path(self, path, tkinker=None, force=False):
        if force or check_dcs_path(path):
            self.config["PATHS"][dcs_config_key] = path
            self.update_tkinker(tkinker, dcs_config_key, path)
            self.load_locales()
            self.save_config()

    def set_loc_needed(self, value: bool):
        self.config["PARAMETERS"][loc_needed_key] = "yes" if value else "no"
        self.save_config()

    def set_loc_enabled(self, locale: str, value: bool):
        self.config["LOCALES"][locale] = "yes" if value else "no"
        self.save_config()

    def save_config(self):
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def load_config(self):
        if os.path.exists("config.ini"):
            self.config.read("config.ini")

        for section in ["PATHS", "PARAMETERS", "LOCALES"]:
            if not self.config.has_section(section):
                self.config.add_section(section)

        if not self.config.has_option("PATHS", sg_config_key) or not self.config.get(
            "PATHS", sg_config_key
        ):
            sg_path = autofill_savedgames_path()
            if sg_path:
                self.set_savedgames_path(sg_path, force=True)

        if not self.config.has_option("PATHS", dcs_config_key) or not self.config.get(
            "PATHS", dcs_config_key
        ):
            dcs_path = autofill_mainfolder_path()
            if dcs_path:
                self.set_dcs_path(dcs_path, force=True)

        if not self.config.has_option("PARAMETERS", loc_needed_key):
            self.set_loc_needed(False)

    def load_locales(self):
        print("Loading locales...")
        locale_folder = os.path.join(self.get_dcs_path(), "l10n")
        locales = [f.name.lower() for f in os.scandir(locale_folder) if f.is_dir()]

        current_locale = Locale.parse(babel.default_locale()).language.lower()
        for locale in locales:
            self.config.set(
                "LOCALES", locale, "yes" if locale == current_locale else "no"
            )

    def get_locales(self):
        return {
            locale: self.config.getboolean("LOCALES", locale)
            for locale in self.config["LOCALES"].keys()
        }

    def print_config(self, msg: str = None):
        if msg:
            print(msg)
        with open("config.ini", "r") as cf:
            print(cf.read())


def check_savedgames_path(path: str):
    if not os.path.isdir(path):
        raise ValueError("DCS Saved Games path is wrong")

    deeper_path = os.path.join(path, "Config/Input")
    if not os.path.isdir(deeper_path):
        raise ValueError("DCS Saved Games folder structure is broken")

    return True


def check_dcs_path(path: str):
    if not os.path.isdir(path):
        raise ValueError("DCS game path is wrong")

    deeper_path = os.path.join(path, "l10n/en/LC_MESSAGES")
    if not os.path.isdir(deeper_path):
        raise ValueError("DCS game path is wrong, 'l10n' folder wasn't found")

    return True


def autofill_savedgames_path():
    default_path = os.path.join(os.getenv("USERPROFILE"), r"Saved Games\DCS")
    try:
        if check_savedgames_path(default_path):
            return default_path
    except ValueError:
        pass

    return None


def autofill_mainfolder_path():
    steam = os.path.join(
        os.getenv("ProgramFiles(x86)"), r"Steam\steamapps\common\DCS World"
    )
    steam_2 = os.path.join(
        os.getenv("ProgramFiles(x86)"), r"Steam\steamapps\common\DCSWorld"
    )
    standalone_x64 = os.path.join(
        os.getenv("ProgramFiles(x86)"), r"Eagle Dynamics\DCS World"
    )
    standalone = os.path.join(os.getenv("ProgramFiles"), r"Eagle Dynamics\DCS World")

    for path in [steam, steam_2, standalone_x64, standalone]:
        try:
            if check_dcs_path(path):
                return path
        except ValueError:
            pass

    return None
