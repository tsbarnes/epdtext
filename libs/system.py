import datetime
import logging
import platform
import time

import distro
import psutil

try:
    # Try to load the network interface setting from local_settings.py
    from local_settings import NETWORK_INTERFACE
except ImportError:
    # Set the default to wlan0
    NETWORK_INTERFACE = "wlan0"


logger = logging.getLogger('pitftmanager.libs.system')


class System:
    """
    This class provides access to system information
    """

    @staticmethod
    def get_size(data, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        :param data: the size in bytes
        :param suffix: which suffix to use as a single letter
        :return the size converted to the proper suffix
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if data < factor:
                return f"{data:.2f}{unit}{suffix}"
            data /= factor

    @property
    def temperature(self):
        return round(psutil.sensors_temperatures()['cpu_thermal'][0].current)

    @property
    def model(self):
        with open('/sys/firmware/devicetree/base/model', 'r') as model_file:
            return model_file.read()

    @property
    def system(self):
        return platform.system()

    @property
    def dist(self):
        return "{0} {1}".format(distro.name(), distro.version())

    @property
    def machine(self):
        return platform.machine()

    @property
    def node(self):
        return platform.node()

    @property
    def arch(self):
        return platform.architecture()[0]

    @property
    def uptime(self):
        return datetime.timedelta(seconds=time.clock_gettime(time.CLOCK_BOOTTIME))

    @property
    def network_total_sent(self):
        net_io = psutil.net_io_counters()
        return self.get_size(net_io.bytes_sent)

    @property
    def network_total_received(self):
        net_io = psutil.net_io_counters()
        return self.get_size(net_io.bytes_recv)

    @property
    def local_ipv4_address(self):
        for interface_name, interface_addresses in psutil.net_if_addrs().items():
            for address in interface_addresses:
                if interface_name == NETWORK_INTERFACE:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        return address.address
        return None

    @property
    def icon(self):
        if distro.id() == 'archarm':
            return "images/arch.png"
        if distro.id() == "manjaro-arm":
            return "images/manjaro.png"
        return "images/raspberry-pi.png"


system = System()


def get_system():
    return system


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Local IPv4 address: {}".format(system.local_ipv4_address))
