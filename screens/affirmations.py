import random
import epd
import settings
import textwrap


class Affirmation:
    affirmations = settings.AFFIRMATIONS
    current_affirmation = affirmations[0]

    def get_random_affirmation(self):
        affirmation = random.choice(self.affirmations)
        while affirmation == self.current_affirmation:
            affirmation = random.choice(self.affirmations)
        self.current_affirmation = affirmation
        return affirmation


affirm = Affirmation()


def print_to_display():
    text = ''
    affirmation = affirm.get_random_affirmation()
    lines = textwrap.wrap(affirmation, width=16)
    for line in lines:
        text += line + '\n'

    epd.print_to_display(text, fontsize=25)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
