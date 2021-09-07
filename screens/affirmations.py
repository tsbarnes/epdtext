import random
import epd


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


def get_random_affirmation():
    return random.choice(affirmations)


def print_to_display():
    epd.print_to_display(get_random_affirmation(), fontsize=25)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
