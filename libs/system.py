import sensors
import logging
import distro
import platform
import time
import datetime
import psutil


try:
    # Try to load the network interface setting from local_settings.py
    from local_settings import NETWORK_INTERFACE
except ImportError:
    # Set the default to wlan0
    NETWORK_INTERFACE = "wlan0"


logger = logging.getLogger('epdtext:libs.system')

class System:
    """
    This class provides access to system information
    """
    temperature_sensor = None
    voltage_sensor = None

    def __init__(self):
        sensors.init()
        for chip in sensors.iter_detected_chips():
            for feature in chip:
                if str(chip) == "cpu_thermal-virtual-0" and feature.label == "temp1":
                    self.temperature_sensor = feature
                elif str(chip) == "rpi_volt-isa-0000" and feature.label == "in0":
                    self.voltage_sensor = feature
        if not self.temperature_sensor:
            logger.warning("Couldn't find temperature sensor")
        if not self.voltage_sensor:
            logger.warning("Couldn't find voltage sensor")

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
        return self.temperature_sensor.get_value()

    @property
    def voltage(self):
        return self.voltage_sensor.get_value()

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


system = System()


def get_system():
    return system


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Local IPv4 address: {}".format(system.local_ipv4_address))
