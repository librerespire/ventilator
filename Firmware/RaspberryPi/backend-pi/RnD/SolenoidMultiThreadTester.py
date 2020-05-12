from datetime import datetime
from PWMController import PWMController
import time
import RPi.GPIO as GPIO
import logging
import logging.config

SOL_I = 21
SOL_E = 20
PWM_PERIOD = 2
threads_map = {}

# declare logger parameters
logger = logging.getLogger(__name__)
logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)


def control_solenoid(pin, duty_ratio):
    # read four pressure sensors from the smbus and return actual values
    logger.debug("Entering control_solenoid()...")
    on_time = PWM_PERIOD * duty_ratio
    off_time = PWM_PERIOD * (1 - duty_ratio)

    if pin in threads_map:
        threads_map[pin].stop()
        threads_map[pin].join()
        logger.debug("Main: Stopped existing thread")

    t = PWMController(datetime.now().strftime('%Y%m%d%H%M%S%f'), pin, on_time, off_time)
    threads_map[pin] = t

    # Don't want these threads to run when the main program is terminated
    t.daemon = True
    t.start()
    logger.debug("Main: Started thread")

    time.sleep(3)

    logger.debug("Leaving control_solenoid().")


######################################################################3

# Initialize digital output pins
GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
GPIO.setup(SOL_I, GPIO.OUT)
GPIO.setup(SOL_E, GPIO.OUT)

while True:
    control_solenoid(SOL_I, 0.8)
    control_solenoid(SOL_E, 0.8)
    time.sleep(2)
