import sensors
import logging
import distro
import platform
import time
import datetime
import psutil


class System:
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
            logging.warning("Couldn't find temperature sensor")
        if not self.voltage_sensor:
            logging.warning("Couldn't find voltage sensor")

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
        suffix = 'B'
        if net_io > 1000000000:
            suffix = 'G'
        elif net_io > 1000000:
            suffix = 'M'
        elif net_io > 1000:
            suffix = 'K'
        return self.get_size(net_io.bytes_sent, suffix)

    @property
    def network_total_received(self):
        net_io = psutil.net_io_counters()
        suffix = 'B'
        if net_io > 1000000000:
            suffix = 'G'
        elif net_io > 1000000:
            suffix = 'M'
        elif net_io > 1000:
            suffix = 'K'
        return self.get_size(net_io.bytes_recv, suffix)


system = System()


def get_system():
    return system
