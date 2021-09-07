import epd
import subprocess
import textwrap


def print_to_display():
    child = subprocess.Popen(['fortune'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    string = child.stdout.read().decode().replace('\n', ' ')
    text = ''
    lines = textwrap.wrap(string, width=40)
    for line in lines:
        text += line + '\n'
    epd.print_to_display(text, fontsize=10, margin=5)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
