from libs.system import System, get_system
from screens import AbstractScreen


class Screen(AbstractScreen):
    system: System = get_system()

    def reload(self) -> None:
        self.blank()
        self.draw_titlebar("Network")

        text = "Local IP: {}".format(self.system.local_ipv4_address) + '\n'
        text += "Total upload: {}".format(self.system.network_total_sent) + '\n'
        text += "Total download: {}".format(self.system.network_total_received)
        self.text(text, font_size=16, position=(5, 30))
