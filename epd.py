import importlib
import logging

from settings import DRIVER
from gpiozero import Button


try:
    driver = importlib.import_module("waveshare_epd." + DRIVER)
except ImportError:
    logging.error("Driver '{0}' couldn't be loaded".format(DRIVER))
    raise ImportError("Couldn't load driver")

epd = driver.EPD()  # get the display
epd.init()  # initialize the display

btns = [Button(5), Button(6), Button(13), Button(19)]


def get_epd():
    return epd


def get_size():
    return driver.EPD_HEIGHT, driver.EPD_WIDTH


def get_buttons():
    return btns


def clear_screen():
    display = get_epd()
    display.Clear(0xFF)
