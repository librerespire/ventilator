import time
import RPi.GPIO as GPIO
import logging
import logging.config

# Constants
SOL_I = 12
SOL_E = 13
PWM_FREQ = 0.5

# declare logger parameters
logger = logging.getLogger(__name__)
logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)


# Initialize digital output pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(SOL_I, GPIO.OUT)
GPIO.setup(SOL_E, GPIO.OUT)

PWM_I = GPIO.PWM(SOL_I, PWM_FREQ)
PWM_E = GPIO.PWM(SOL_E, PWM_FREQ)

PWM_I.start(0)
PWM_E.start(0)

while True:

    # inspiratory phase
    logger.debug("Enter inspiratory")
    PWM_I.ChangeDutyCycle(100)
    PWM_E.ChangeDutyCycle(0)
    time.sleep(2)
    logger.debug("Leave inspiratory\n")

    # expiratory phase
    logger.debug("Enter expiratory")
    PWM_I.ChangeDutyCycle(0)
    PWM_E.ChangeDutyCycle(100)
    time.sleep(2)
    logger.debug("Leave inspiratory\n")

    # waiting phase
    logger.debug("Enter waiting")
    PWM_I.ChangeDutyCycle(0)
    PWM_E.ChangeDutyCycle(0)
    time.sleep(1)
    logger.debug("Leave waiting\n")
