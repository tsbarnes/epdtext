import datetime
import logging
import os
import platform
import time

import distro
import humanize
from PIL import Image

import settings
from screens import AbstractScreen
from settings import LOGO


class Screen(AbstractScreen):
    def reload(self):
        self.blank()
        self.draw_titlebar("System/Uptime")

        logo = Image.open(LOGO)
        self.image.paste(logo, (100, 25))

        string = ''
        with open('/sys/firmware/devicetree/base/model', 'r') as model_file:
            model = model_file.read()
            string += model + '\n'

        self.text(string, font_size=14, font_name=settings.BOLD_FONT, position=(5, 75), wrap=False)

        string = ''

        dist = "{0} {1}".format(distro.name(), distro.version())
        string += 'OS:      ' + dist + '\n'

        string += 'Machine: ' + platform.machine() + '\n'
        string += 'Node:    ' + platform.node() + '\n'

        uptime = datetime.timedelta(seconds=time.clock_gettime(time.CLOCK_BOOTTIME))
        string += 'Uptime:  ' + humanize.naturaldelta(uptime)

        self.text(string, font_size=14, font_name=settings.MONOSPACE_FONT, position=(5, 90), wrap=False)

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
