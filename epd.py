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


def print_to_display(string, font=settings.FONT, fontsize=20, margin=5):
    display = get_epd()

    text = ''
    line_width = (get_size()[1] / (fontsize / 2.5))
    logging.debug("Horizontal size: {0}, font size: {1}, line wrap: {2}".format(get_size()[1], fontsize, line_width))
    for string_line in string.split('\n'):
        lines = textwrap.wrap(string_line, width=line_width)
        for line in lines:
            text += line + '\n'

    h_black_image = Image.new('1', get_size(), 255)
    h_red_image = Image.new('1', get_size(), 255)
    # Create draw object and pass in the image layer we want to work with (HBlackImage)
    draw = ImageDraw.Draw(h_black_image)
    # Create our font, passing in the font file and font size
    font = ImageFont.truetype(font, fontsize)
    draw.text((margin, margin), text, font=font, fill=0)
    display.display(display.getbuffer(h_black_image), display.getbuffer(h_red_image))


def clear_screen():
    display = get_epd()
    display.Clear(0xFF)
