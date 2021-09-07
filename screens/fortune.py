import epd
import subprocess


def print_to_display():
    child = subprocess.Popen(['fortune'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    string = child.stdout.read().decode()
    epd.print_to_display(string, fontsize=10)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
