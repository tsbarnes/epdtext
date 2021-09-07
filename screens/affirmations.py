import random
import epd


class Affirmation:
    affirmations = [
        "You are\nenough",
        "You are loved",
        "You are safe",
        "Be yourself",
        "They can't\nhurt you\nanymore",
        "You are\nbeautiful",
        "You are\nstrong",
        "You have\ncome a\nlong way"
    ]
    current_affirmation = affirmations[0]

    def get_random_affirmation(self):
        affirmation = random.choice(self.affirmations)
        while affirmation == self.current_affirmation:
            affirmation = random.choice(self.affirmations)
        self.current_affirmation = affirmation
        return affirmation


affirm = Affirmation()


def print_to_display():
    epd.print_to_display(affirm.get_random_affirmation(), fontsize=25)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
