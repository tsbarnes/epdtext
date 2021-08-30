import time
import random
from PIL import Image, ImageDraw, ImageFont

import epd
from settings import FONT


def print_to_display(string):
    display = epd.get_epd()
    h_black_image = Image.new('1', epd.get_size(), 255)
    h_red_image = Image.new('1', epd.get_size(), 255)
    # Create draw object and pass in the image layer we want to work with (HBlackImage)
    draw = ImageDraw.Draw(h_black_image)
    # Create our font, passing in the font file and font size
    font = ImageFont.truetype(FONT, 30)
    draw.text((25, 25), string, font = font, fill = 0)
    display.display(display.getbuffer(h_black_image), display.getbuffer(h_red_image))


affirmations = [
    "You are\nenough",
    "You are loved",
    "You are safe",
    "Be yourself",
    "They can't\nhurt you\nanymore",
    "You are\nbeautiful",
    "You are\nstrong",
]


def handle_btn_press():
    print_to_display(random.choice(affirmations))
