import time
import datetime
import platform
import epd
import humanize


def print_to_display():
    dist = " ".join(x for x in platform.dist())
    uptime = datetime.timedelta(seconds=time.clock_gettime(time.CLOCK_BOOTTIME))
    string = ''
    string += '\tSystem:  ' + platform.system() + '\n'
    string += '\tDistrib: ' + dist + '\n'
    string += '\tMachine: ' + platform.machine() + '\n'
    string += '\tNode:    ' + platform.node() + '\n'
    string += '\tArch:    ' + platform.architecture()[0] + '\n'
    string += '\tUptime:\n' + humanize.naturaldelta(uptime)
    epd.print_to_display(string, fontsize=16)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
