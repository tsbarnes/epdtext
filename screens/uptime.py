import os
import time
import datetime
import platform
import humanize
import logging
from PIL import Image, ImageDraw, ImageFont
from settings import FONT, LOGO
from screens import AbstractScreen


class Screen(AbstractScreen):
    def reload(self):
        self.blank()

        logo = Image.open(LOGO)
        self.image.paste(logo, (100, 5))

        # Create draw object and pass in the image layer we want to work with (HBlackImage)
        draw = ImageDraw.Draw(self.image)
        # Create our font, passing in the font file and font size
        font = ImageFont.truetype(FONT, 14)

        string = ''

        with open('/sys/firmware/devicetree/base/model', 'r') as model_file:
            model = model_file.read()
            string += model + '\n'

        string += ' System:  ' + platform.system() + '\n'

        dist = " ".join(x for x in platform.dist())
        string += ' OS:      ' + dist + '\n'

        string += ' Machine: ' + platform.machine() + '\n'
        string += ' Node:    ' + platform.node() + '\n'
        string += ' Arch:    ' + platform.architecture()[0] + '\n'

        uptime = datetime.timedelta(seconds=time.clock_gettime(time.CLOCK_BOOTTIME))
        string += ' Uptime:  ' + humanize.naturaldelta(uptime)

        draw.text((5, 50), string, font=font, fill=0)

    def handle_btn_press(self, button_number=1):
        if button_number == 1:
            self.reload()
        elif button_number == 2:
            logging.info("Rebooting...")
            os.system("sudo reboot now")
