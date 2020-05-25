import smbus
import time
import bme680
from Variables import Variables


class SensorReader:
    bus = None
    delay = 0.05
    pressure = -0
    cTemp = 999
    fTemp = 999
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
            return self.convert_pressure(sensor.data.pressure)

    def read_temp(self):
        #Reading Data from i2c bus 3
        b1 = self.bus.read_i2c_block_data(0x76, 0x88, 24)
        # Convert the data
        # Temp coefficents
        dig_T1 = b1[1] * 256 + b1[0]
        dig_T2 = b1[3] * 256 + b1[2]
        if dig_T2 > 32767 :
            dig_T2 -= 65536
        dig_T3 = b1[5] * 256 + b1[4]
        if dig_T3 > 32767 :
            dig_T3 -= 65536
        # BMP280 address, 0x76(118)
        # Select Control measurement register, 0xF4(244)
        #		0x27(39)	Pressure and Temperature Oversampling rate = 1
        #					Normal mode
        self.bus.write_byte_data(0x76, 0xF4, 0x27)
        # BMP280 address, 0x76(118)
        # Select Configuration register, 0xF5(245)
        #		0xA0(00)	Stand_by time = 1000 ms
        self.bus.write_byte_data(0x76, 0xF5, 0xA0)
        time.sleep(self.delay)
        # BMP280 address, 0x76(118)
        # Read data back from 0xF7(247), 8 bytes
        # Pressure MSB, Pressure LSB, Pressure xLSB, Temperature MSB, Temperature LSB
        # Temperature xLSB, Humidity MSB, Humidity LSB
        data = self.bus.read_i2c_block_data(0x76, 0xF7, 8)
        # Convert temperature data to 19-bits
        adc_t = ((data[3] * 65536) + (data[4] * 256) + (data[5] & 0xF0)) / 16
        # Temperature offset calculations
        var1 = ((adc_t) / 16384.0 - (dig_T1) / 1024.0) * (dig_T2)
        var2 = (((adc_t) / 131072.0 - (dig_T1) / 8192.0) * ((adc_t)/131072.0 - (dig_T1)/8192.0)) * (dig_T3)
        t_fine = (var1 + var2)
        self.cTemp = (var1 + var2) / 5120.0
        self.fTemp = self.cTemp * 1.8 + 32

    def read_pressure(self):

        # For demo p3 is read from a bme680 sensor
        if Variables.demo and self.bus_number == Variables.BUS_3:
            self.pressure = self.read_bme680() - self.get_offset()
            return self.pressure

        #Reading Data from i2c bus 3
        b1 = self.bus.read_i2c_block_data(0x76, 0x88, 24)
        # Convert the data
        # Temp coefficents
        dig_T1 = b1[1] * 256 + b1[0]
        dig_T2 = b1[3] * 256 + b1[2]
        if dig_T2 > 32767 :
            dig_T2 -= 65536
        dig_T3 = b1[5] * 256 + b1[4]
        if dig_T3 > 32767 :
            dig_T3 -= 65536
        # Pressure coefficents
        dig_P1 = b1[7] * 256 + b1[6]
        dig_P2 = b1[9] * 256 + b1[8]
        if dig_P2 > 32767 :
            dig_P2 -= 65536
        dig_P3 = b1[11] * 256 + b1[10]
        if dig_P3 > 32767 :
            dig_P3 -= 65536
        dig_P4 = b1[13] * 256 + b1[12]
        if dig_P4 > 32767 :
            dig_P4 -= 65536
        dig_P5 = b1[15] * 256 + b1[14]
        if dig_P5 > 32767 :
            dig_P5 -= 65536
        dig_P6 = b1[17] * 256 + b1[16]
        if dig_P6 > 32767 :
            dig_P6 -= 65536
        dig_P7 = b1[19] * 256 + b1[18]
        if dig_P7 > 32767 :
            dig_P7 -= 65536
        dig_P8 = b1[21] * 256 + b1[20]
        if dig_P8 > 32767 :
            dig_P8 -= 65536
        dig_P9 = b1[23] * 256 + b1[22]
        if dig_P9 > 32767 :
            dig_P9 -= 65536
        # BMP280 address, 0x76(118)
        # Select Control measurement register, 0xF4(244)
        #		0x27(39)	Pressure and Temperature Oversampling rate = 1
        #					Normal mode
        self.bus.write_byte_data(0x76, 0xF4, 0x27)
        # BMP280 address, 0x76(118)
        # Select Configuration register, 0xF5(245)
        #		0xA0(00)	Stand_by time = 1000 ms
        self.bus.write_byte_data(0x76, 0xF5, 0xA0)
        time.sleep(self.delay)
        # BMP280 address, 0x76(118)
        # Read data back from 0xF7(247), 8 bytes
        # Pressure MSB, Pressure LSB, Pressure xLSB, Temperature MSB, Temperature LSB
        # Temperature xLSB, Humidity MSB, Humidity LSB
        data = self.bus.read_i2c_block_data(0x76, 0xF7, 8)
        # Convert pressure data to 19-bits
        adc_p = ((data[0] * 65536) + (data[1] * 256) + (data[2] & 0xF0)) / 16
        adc_t = ((data[3] * 65536) + (data[4] * 256) + (data[5] & 0xF0)) / 16
        # Temperature offset calculations
        var1 = ((adc_t) / 16384.0 - (dig_T1) / 1024.0) * (dig_T2)
        var2 = (((adc_t) / 131072.0 - (dig_T1) / 8192.0) * ((adc_t)/131072.0 - (dig_T1)/8192.0)) * (dig_T3)
        t_fine = (var1 + var2)
        # Pressure offset calculations
        var1 = (t_fine / 2.0) - 64000.0
        var2 = var1 * var1 * (dig_P6) / 32768.0
        var2 = var2 + var1 * (dig_P5) * 2.0
        var2 = (var2 / 4.0) + ((dig_P4) * 65536.0)
        var1 = ((dig_P3) * var1 * var1 / 524288.0 + ( dig_P2) * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * (dig_P1)
        p = 1048576.0 - adc_p
        p = (p - (var2 / 4096.0)) * 6250.0 / var1
        var1 = (dig_P9) * p * p / 2147483648.0
        var2 = p * (dig_P8) / 32768.0
        self.pressure = ((p + (var1 + var2 + dig_P7) / 16.0) / 100) - self.get_offset()
        return self.pressure
        # Output data to screen ** uncomment this part to see values form sensors
        # print("""\t======== bus %d ==========
        # Temperature in Celsius : %.2f C
        # Temperature in Fahrenheit : %.2f F
        # Pressure : %.2f hPa
        # Time: %s
        # =======================\n""" % (self.bus_number, self.cTemp,
        #             self.fTemp,
        #             self.pressure,
        #             datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))

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
