import inspect
import logging
import os
import pathlib
from collections import Generator


def get_screens():
    screens: list = []

    path: str = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    screen_directory: Generator[pathlib.Path, None, None] = pathlib.Path(path).rglob("*.py")

    for file in screen_directory:
        if file.name == "__init__.py":
            continue
        module_name = file.name.split(".")[0]
        logging.debug("Found '{0}' in '{1}'".format(module_name, path))
        screens.append(module_name)

    return screens
