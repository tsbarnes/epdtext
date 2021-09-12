import random
import epd
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
        text = self.get_random_affirmation()
        epd.print_to_display(text, fontsize=25)

    def handle_btn_press(self, button_number=1):
        if button_number == 1:
            self.reload()
        elif button_number == 2:
            pass
