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

pwm_i = GPIO.PWM(SOL_I, PWM_FREQ)
pwm_e = GPIO.PWM(SOL_E, PWM_FREQ)

pwm_i.start(0)
pwm_e.start(0)

while True:

    # inspiratory phase
    logger.debug("Enter inspiratory")
    pwm_i.ChangeDutyCycle(80)
    pwm_e.ChangeDutyCycle(0)
    time.sleep(2)
    logger.debug("Leave inspiratory\n")

    # expiratory phase
    logger.debug("Enter expiratory")
    pwm_i.ChangeDutyCycle(0)
    pwm_e.ChangeDutyCycle(100)
    time.sleep(2)
    logger.debug("Leave inspiratory\n")

    # waiting phase
    logger.debug("Enter waiting")
    pwm_i.ChangeDutyCycle(0)
    pwm_e.ChangeDutyCycle(0)
    time.sleep(1)
    logger.debug("Leave waiting\n")
