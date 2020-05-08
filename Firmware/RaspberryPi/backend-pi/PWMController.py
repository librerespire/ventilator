import threading
import time
import RPi.GPIO as GPIO


class PWMController(threading.Thread):
    """ Thread class with a stop() method.
        Handy class to implement PWM on digital output pins """

    def __init__(self, thread_id, pin, on_time, off_time):
        threading.Thread.__init__(self)
        self.__thread_id = thread_id
        self.__pin = pin
        self.__on_time = on_time
        self.__off_time = off_time
        self.__stop_event = threading.Event()

        # TODO: Setting up the pins should be moved to the main script 'Controller.py'
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin, GPIO.OUT)

    def stop(self):
        self.__stop_event.set()
        # print(str(self.__thread_id) + ": set the stop event")

    def stopped(self):
        return self.__stop_event.is_set()

    def run(self):
        while True:
            if self.stopped():
                # print(str(self.__thread_id) + ": thread has stopped. exiting")
                break;
            # print(str(self.__thread_id) + ": ON--")
            if self.__on_time > 0.02:
                GPIO.output(self.__pin, GPIO.HIGH)
                time.sleep(self.__on_time)
            # print(str(self.__thread_id) + ": OFF--")
            if self.__off_time > 0.02:
                GPIO.output(self.__pin, GPIO.LOW)
                time.sleep(self.__off_time)
