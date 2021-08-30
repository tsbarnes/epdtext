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
]


def get_random_affirmation():
    return random.choice(affirmations)


def print_to_display():
    epd.print_to_display(get_random_affirmation(), fontsize=30)


def handle_btn_press():
    print_to_display()
