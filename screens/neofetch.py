import epd
import subprocess


def print_to_display():
    child = subprocess.Popen(['neofetch'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    string = child.stdout.read().decode().replace('\n', ' ')
    epd.print_to_display(string, fontsize=10, margin=5)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
