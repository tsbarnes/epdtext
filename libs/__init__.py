import inspect
import logging
import os
import pathlib
from collections import Generator


logger = logging.getLogger('epdtext:libs')


def get_libs():
    libs: list = []

    path: str = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    lib_directory: Generator[pathlib.Path, None, None] = pathlib.Path(path).rglob("*.py")

    for file in lib_directory:
        if file.name == "__init__.py":
            continue
        module_name = file.name.split(".")[0]
        logger.debug("Found '{0}' in '{1}'".format(module_name, path))
        libs.append(module_name)

    return libs
