import os
import time
import datetime
import platform
import epd
import humanize
import logging
from PIL import Image, ImageDraw, ImageFont
from settings import FONT, LOGO


def print_to_display():
    display = epd.get_epd()

    h_black_image = Image.new('1', epd.get_size(), 255)
    h_red_image = Image.new('1', epd.get_size(), 255)

    logo = Image.open(LOGO)
    h_black_image.paste(logo, (100, 5))

    # Create draw object and pass in the image layer we want to work with (HBlackImage)
    draw = ImageDraw.Draw(h_black_image)
    # Create our font, passing in the font file and font size
    font = ImageFont.truetype(FONT, 14)

    string = ''

    with open('/sys/firmware/devicetree/base/model', 'r') as model_file:
        model = model_file.read()
        string += model + '\n'

    string += '\tSystem:  ' + platform.system() + '\n'

    dist = " ".join(x for x in platform.dist())
    string += '\tOS:      ' + dist + '\n'

    string += '\tMachine: ' + platform.machine() + '\n'
    string += '\tNode:    ' + platform.node() + '\n'
    string += '\tArch:    ' + platform.architecture()[0] + '\n'

    uptime = datetime.timedelta(seconds=time.clock_gettime(time.CLOCK_BOOTTIME))
    string += '\tUptime:  ' + humanize.naturaldelta(uptime)

    draw.text((5, 50), string, font=font, fill=0)
    display.display(display.getbuffer(h_black_image), display.getbuffer(h_red_image))


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        logging.info("Rebooting...")
        os.system("sudo reboot now")


def iterate_loop():
    pass
