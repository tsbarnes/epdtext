import random
import time
import epd

import affirmations as af


class App:
    last_pressed = 0

    def handle_btn0_press(self):
        self.last_pressed = 0
        af.handle_btn_press()

    def __init__(self):
        btns = epd.get_buttons()
        btns[0].when_pressed = self.handle_btn0_press

    def loop(self):
        while True:
            if self.last_pressed == 0:
                af.print_to_display(random.choice(af.affirmations))
            time.sleep(500)


if __name__ == '__main__':
    app = App()
    app.loop()
