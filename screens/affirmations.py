import random

import settings
from screens import AbstractScreen


class Screen(AbstractScreen):
    affirmations = settings.AFFIRMATIONS
    current_affirmation = affirmations[0]

    def get_random_affirmation(self):
        affirmation = random.choice(self.affirmations)
        while affirmation == self.current_affirmation:
            affirmation = random.choice(self.affirmations)
        self.current_affirmation = affirmation
        return affirmation

    def reload(self):
        self.blank()
        self.text("Affirmations", font_size=20, position=(0, 0))
        self.line((0, 25, self.display.get_size()[0], 25), width=1)
        text = self.get_random_affirmation()
        self.text(text, font_size=25, position=(5, 30))

    def handle_btn_press(self, button_number=1):
        if button_number == 1:
            self.reload()
            self.show()
        elif button_number == 2:
            pass
