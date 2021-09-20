import datetime
import logging
import os
import platform
import time

import distro
import humanize
from PIL import Image, ImageDraw, ImageFont

from screens import AbstractScreen
from settings import FONT, LOGO


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

        dist = "{0} {1}".format(distro.name(), distro.version())
        string += ' OS:      ' + dist + '\n'

        string += ' Machine: ' + platform.machine() + '\n'
        string += ' Node:    ' + platform.node() + '\n'
        string += ' Arch:    ' + platform.architecture()[0] + '\n'

        uptime = datetime.timedelta(seconds=time.clock_gettime(time.CLOCK_BOOTTIME))
        string += ' Uptime:  ' + humanize.naturaldelta(uptime)

        draw.text((5, 55), string, font=font, fill=0)

    def handle_btn_press(self, button_number=1):
        if button_number == 1:
            self.reload()
            self.show()
        elif button_number == 2:
            logging.info("Rebooting...")
            self.blank()
            self.text("Rebooting...", font_size=30)
            self.show()
            os.system("sudo reboot now")
