import threading
import time
# import RPi.GPIO as GPIO

class PWMController(threading.Thread):
    """ Thread class with a stop() method.
        Handy class to implement PWM on digital output pins """

    def __init__(self, pin, on_time, off_time):
        threading.Thread.__init__(self)
        self.__pin = pin
        self.__on_time = on_time
        self.__off_time = off_time
        self.__stop_event = threading.Event()

    def stop(self):
        self.__stop_event.set()
        print(str(threading.get_ident()) + ": set the stop event")

    def stopped(self):
        return self.__stop_event.is_set()

    def run(self):
        while True:
            if self.stopped():
                print(str(threading.get_ident()) + ": thread has stopped. exiting")
                break;
            print(str(threading.get_ident()) + ": ON--")
            # GPIO.output(self.__pin, GPIO.HIGH)
            time.sleep(self.__on_time)
            print(str(threading.get_ident()) + ": OFF--")
            # GPIO.output(self.__pin, GPIO.LOW)
            time.sleep(self.__off_time)