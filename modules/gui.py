from tkinter import (
    BooleanVar,
    StringVar,
    Tk,
    messagebox,
)

from tkinter import ttk
from tkinter.ttk import Checkbutton, Frame, Button, Label
import sv_ttk

from tkinter.filedialog import askdirectory

from modules.config import Config
from modules.templater import Templater


class Vars:
    def __init__(self, config: Config):
        self.vars: dict[str, StringVar | BooleanVar] = {}
        self.config = config

    def add_config_link(
        self, section: str, key: str, fallback=None, vartype=StringVar, type=str
    ):
        self.vars[key] = (vartype)(
            value=self.config.get(section, key, fallback=fallback, type=type)
        )
        return self.vars[key]

    def get(self, key: str):
        return self.vars[key]

    def set(self, key: str, value):
        self.vars[key].set(value)


class TemplaterApp(Tk):
    def __init__(self, config: Config, templater: Templater, open_path):
        super().__init__()
        self.config = config
        self.vars = Vars(config)
        self.open_path = open_path

        self.title("DCS Templater")
        # self.geometry("800x800")

        # Saved Games Folder
        sg_frame = Frame(self)
        sg_frame.pack(fill="x", padx=5, pady=5)

        sg_title = Label(sg_frame, text="Saved Games Folder:", anchor="w")
        sg_title.grid(sticky="w", column=0, columnspan=2)

        sg_var = self.vars.add_config_link(
            "PATHS", "dcs_savedgames", "Please select DCS folder in Saved Games"
        )

        sg_folder = Label(
            sg_frame,
            textvariable=(sg_var),
            anchor="w",
        )
        sg_folder.grid(sticky="w", row=1, column=0)

        btn_sg_folder_select = Button(
            sg_frame, text="Set Folder", command=self.select_sg_folder
        )
        btn_sg_folder_select.grid(row=1, column=1)

        sg_frame.columnconfigure(0, weight=1)

        # Localization
        s = ttk.Style()
        s.configure("loc_frame.TFrame", background="red")
        loc_frame = Frame(self, style="loc_frame.TFrame")
        loc_frame.pack(fill="x", padx=5, pady=10, anchor="ne")

        loc_cb_var = self.vars.add_config_link(
            "PARAMETERS", "loc_needed", False, vartype=BooleanVar, type=bool
        )

        loc_cb = Checkbutton(
            loc_frame,
            text="Translate",
            variable=loc_cb_var,
            command=self.loc_toggle,
        )
        loc_cb.pack(fill="x", anchor="w")

        # Locale List
        loc_subframe = Frame(loc_frame)
        self.loc_subframe = loc_subframe
        loc_subframe.pack(fill="x")

        locales = Frame(loc_subframe)
        locale_dict = self.config.get_locales()

        for locale, locale_bool in locale_dict.items():
            locale_var = BooleanVar(value=locale_bool)
            self.vars.vars[f"loc_{locale}"] = locale_var
            locale_cb = Checkbutton(
                locales,
                variable=locale_var,
                text=locale,
                command=lambda locale=locale: self.set_loc_var(locale),
            )
            locale_cb.pack(side="left", padx=0)

        locales.grid(column=0, columnspan=2, sticky="w", pady=4)

        # Locale Folder
        loc_title = Label(loc_subframe, text="DCS Game Folder:", anchor="w")
        loc_title.grid(sticky="w", row=1, column=0, columnspan=2)

        dcs_var = self.vars.add_config_link(
            "PATHS", "dcs_folder", "Please Select DCS main game folder"
        )

        loc_folder = Label(loc_subframe, textvariable=dcs_var, anchor="w")
        loc_folder.grid(sticky="w", row=2, column=0)

        btn_loc_folder_select = Button(
            loc_subframe, text="Set Folder", command=self.select_dcs_folder
        )
        btn_loc_folder_select.grid(row=2, column=1)
        loc_subframe.columnconfigure(0, weight=1)

        if not loc_cb_var.get():
            self.loc_subframe.pack_forget()

        # Footer
        footer = Frame(
            self,
        )
        footer.pack(fill="both", expand=True, pady=(15, 5), padx=5, anchor="sw")

        # Generate Btn
        btn_generate = Button(
            footer,
            text="Generate",
            command=templater.generate_templates,
            style="Gen.TButton",
        )
        btn_generate.pack(side="right", anchor="sw")

        # Open Folder Btn
        s.configure("Gen.TButton", weight="bold", padding=5)
        btn_open = Button(
            footer,
            text="Open Renders",
            command=open_path,
            style="Gen.TButton",
        )
        btn_open.pack(side="right", padx=5, anchor="sw")

        self.minsize(450, 100)
        sv_ttk.set_theme("dark")

    def set_loc_var(self, locale: str):
        loc_value = self.vars.get(f"loc_{locale}").get()
        self.config.set_loc_enabled(locale, loc_value)

    def loc_toggle(self):
        loc_value = self.vars.get("loc_needed").get()
        self.config.set_loc_needed(loc_value)
        if loc_value:
            self.loc_subframe.pack(fill="x")
        else:
            self.loc_subframe.pack_forget()

    def select_sg_folder(self):
        directory = askdirectory()
        if directory:
            try:
                self.config.set_savedgames_path(directory, tkinker=self)
            except ValueError as e:
                messagebox.showerror(
                    "Error - Wrong Folder",
                    (
                        "Please select DCS folder in Saved Games directory,"
                        "it should contain 'Config' folder with 'Input' folder inside it"
                    ),
                    detail=e,
                )

    def select_dcs_folder(self):
        directory = askdirectory()
        if directory:
            try:
                self.config.set_dcs_path(directory, tkinker=self)
            except ValueError as e:
                messagebox.showerror(
                    "Error - Wrong Folder",
                    (
                        "Please select DCS installation folder, it should contain 'I10n' folder."
                        "Do not select bin or bin-mt folders, select the whole 'DCS World'"
                    ),
                    detail=e,
                )
