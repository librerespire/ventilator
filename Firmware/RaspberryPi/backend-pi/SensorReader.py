import smbus
import time
import bme680
import bmp280
from Variables import Variables


class SensorReader:
    bus = None
    pressure = -0
    bus_number = 0

    def __init__(self, bus_number):
        # Get I2C
        self.bus_number = bus_number
        self.bus = smbus.SMBus(self.bus_number)

    def read_bme680(self):
        try:
            sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY, self.bus)
        except IOError:
            sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY, self.bus)
        sensor.set_pressure_oversample(bme680.OS_4X)
        if sensor.get_sensor_data():
            return sensor.data.pressure

    def read_bmp280(self):
        try:
            sensor = bmp280.BMP280(bmp280.I2C_ADDRESS_GND, self.bus)
        except IOError:
            sensor = bmp280.BMP280(bmp280.I2C_ADDRESS_VCC, self.bus)
        return sensor.get_pressure()

    def read_pressure(self):

        # For demo, p3 is read from a bme680 sensor
        if Variables.demo and self.bus_number == Variables.BUS_3:
            self.pressure = self.read_bme680() - self.get_offset()
        else:
            self.pressure = self.read_bmp280() - self.get_offset()

        return self.pressure


    def convert_pressure(self, p_hpa):
        """ returns inspiratory pressure relative to atm in cmH2O"""
        return (p_hpa * 1.0197442) - 1033.23

    def get_offset(self):
        if self.bus_number is Variables.BUS_1:
            offset = Variables.p1_offset
        elif self.bus_number is Variables.BUS_2:
            offset = Variables.p2_offset
        elif self.bus_number is Variables.BUS_3:
            offset = Variables.p3_offset
        elif self.bus_number is Variables.BUS_4:
            offset = Variables.p4_offset
        return offset

    def get_pressure(self):
        self.read_pressure()
        return self.pressure

    def get_ftemp(self):
        self.read_temp(self)
        return self.fTemp

    def get_ctemp(self):
        self.read_temp(self)
        return self.cTemp
