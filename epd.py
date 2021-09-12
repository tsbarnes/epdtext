from waveshare_epd import epd2in7b
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
import settings
import textwrap
import logging


epd = epd2in7b.EPD()  # get the display
epd.init()  # initialize the display

btns = [Button(5), Button(6), Button(13), Button(19)]


def get_epd():
    return epd


def get_size():
    return epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH


def get_buttons():
    return btns


def clear_screen():
    display = get_epd()
    display.Clear(0xFF)
