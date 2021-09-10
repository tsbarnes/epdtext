import epd
import subprocess
import logging


def print_to_display():
    try:
        child = subprocess.Popen(['/usr/games/fortune'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        string = child.stdout.read().decode().replace('\n', ' ')
    except OSError:
        logging.error("couldn't run application 'fortune'")
        string = ''
    epd.print_to_display(string, fontsize=14, margin=5)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass


def iterate_loop():
    pass
