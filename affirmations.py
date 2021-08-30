import time
import random
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in7b
from gpiozero import Button


def print_to_display(string):
    h_black_image = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)
    h_red_image = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)
    # Create draw object and pass in the image layer we want to work with (HBlackImage)
    draw = ImageDraw.Draw(h_black_image)
    # Create our font, passing in the font file and font size
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
    draw.text((25, 25), string, font = font, fill = 0)
    epd.display(epd.getbuffer(h_black_image), epd.getbuffer(h_red_image))


affirmations = [
    "You are\nenough",
    "You are loved",
    "You are safe",
    "Be yourself",
    "They can't\nhurt you\nanymore",
    "You are\nbeautiful",
    "You are\nstrong",
]

epd = epd2in7b.EPD()  # get the display
epd.init()            # initialize the display

btn = Button(5)


def handle_btn_press():
    print_to_display(random.choice(affirmations))


btn.when_pressed = handle_btn_press


while True:
    print_to_display(random.choice(affirmations))
    time.sleep(500)
