import sensors
import logging
import distro
import platform
import time
import datetime


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


system = System()


def get_system():
    return system
