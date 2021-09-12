import epd
import subprocess
import logging
from screens import AbstractScreen


class Screen(AbstractScreen):
    def reload(self):
        try:
            child = subprocess.Popen(['/usr/games/fortune'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            string = child.stdout.read().decode().replace('\n', ' ')
        except OSError:
            logging.error("couldn't run application 'fortune'")
            string = ''
        epd.print_to_display(string, fontsize=14, margin=5)

    def handle_btn_press(self, button_number=1):
        if button_number == 1:
            self.reload()
        elif button_number == 2:
            pass
