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
# GPIO.setup(SOL_E, GPIO.OUT)

pwm_i = GPIO.PWM(SOL_I, PWM_FREQ)
# pwm_e = GPIO.PWM(SOL_E, PWM_FREQ)

pwm_i.start(0)
# pwm_e.start(0)

pwm_i.ChangeDutyCycle(0.2)
# pwm_e.ChangeDutyCycle(0.8)

d = 0;

while True:
    d += 1
    pwm_i.ChangeDutyCycle(0.2)
    # pwm_e.ChangeDutyCycle(0.8)
    time.sleep(1)
    if d > 99:
        d = 0
    pass

# while True:
#     pwm_i.ChangeDutyCycle(0.8)
#     pwm_e.ChangeDutyCycle(0.8)
#     time.sleep(2)
