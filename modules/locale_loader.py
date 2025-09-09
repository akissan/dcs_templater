import gettext
from os import path
from modules.config import Config, dcs_config_key


class LocaleManager:
    def __init__(self, config: Config):
        self.config = config
        self.locale_folder = path.join(self.config.get("PATHS", dcs_config_key), "l10n")
        self.en_translation = self.load_en_gnutranslation()
        self.reverse_mapping = {v: k for k, v in self.en_translation._catalog.items()}
        self.locales = self.load_locales()

    def load_en_gnutranslation(self):
        en_loc_path = path.join(
            self.locale_folder,
            r"en\LC_MESSAGES\input.mo",
        )
        if not path.isfile(en_loc_path):
            raise RuntimeError("Can't load en localization file")

        en_loc = gettext.GNUTranslations(open(en_loc_path, "rb"))
        return en_loc

    def reverse_loc(self, term: str):
        return self.reverse_mapping[term]

    def load_locales(self):
        locale_dict = self.config.get_locales()

        locales = {
            language: gettext.translation(
                "input",
                localedir=self.locale_folder,
                languages=[language],
            ).gettext
            for language in locale_dict.keys()
        }
        print(locales)

        return locales

    def loc(self, key: str, locale: str):
        return self.locales[locale][key]
