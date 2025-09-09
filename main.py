import os
import webbrowser
from modules.config import Config
from modules.gui import TemplaterApp
from modules.templater import Templater


def open_renders():
    webbrowser.open(os.path.realpath(r"Templates\renders"))


if __name__ == "__main__":
    config = Config()
    templater = Templater(config)
    app = TemplaterApp(config, templater, open_renders)
    app.mainloop()
