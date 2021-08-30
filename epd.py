from waveshare_epd import epd2in7b
from gpiozero import Button


epd = epd2in7b.EPD()  # get the display
epd.init()  # initialize the display

btns = [Button(5)]


def get_epd():
    return epd


def get_size():
    return epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH


def get_buttons():
    return btns
