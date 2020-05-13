import time
from SensorReader import SensorReader
from Variables import Variables
import threading
import logging
import logging.config

logger = logging.getLogger(__name__)
logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)

class SensorReaderService:
    """
    This class can use for probe sensors periodically with the delay 0.01
    sensor_reader() will set pressure values in to Variables class
    """
    pressure_data = [0] * 6
    delay = 0.01
    loop_flag = 1

    def __init__(self):
        self.sensor_reader()

    def set_loop_flag(self, flag):
        if (flag != 0 ):
            self.loop_flag = 1
        else:
            self.loop_flag = 0

    def thread_slice(self, pressure_data, index):
        sr = SensorReader(index)
        pressure = sr.read_pressure()
        pressure_data[index] = pressure

    def sensor_reader(self):
        while self.loop_flag:
            threads = list()
            for index in [Variables.BUS_1, Variables.BUS_2, Variables.BUS_3, Variables.BUS_4]:
                thread = threading.Thread(
                    target=self.thread_slice, args=(self.pressure_data, index,))
                threads.append(thread)
                thread.start()
            for index, thread in enumerate(threads):
                thread.join()
            logger.debug("Pressure: P1[%.2f], P2[%.2f], P3[%.2f], P4[%.2f]" %
                         (self.pressure_data[Variables.BUS_1], self.pressure_data[Variables.BUS_2],
                         self.pressure_data[Variables.BUS_3], self.pressure_data[Variables.BUS_4]))
            Variables.p1 = self.pressure_data[Variables.BUS_1]
            Variables.p2 = self.pressure_data[Variables.BUS_2]
            Variables.p3 = self.pressure_data[Variables.BUS_3]
            Variables.p4 = self.pressure_data[Variables.BUS_4]
            time.sleep(self.delay)

if __name__ == "__main__":
    s = SensorReaderService()
    time.sleep(10)
    s.set_loop_flag(0)
