import sys
sys.path.append('..')

from PID import PID
from SensorReaderService import SensorReaderService
from Variables import Variables
import time
from os import path
import RPi.GPIO as GPIO

# Constants
PWM_FREQ = 2  # frequency for PWM
SO_PIN = 13   # PIN (PWM) for O2 intake solenoid
SI_PIN = 12   # PIN (PWM) for inspiratory solenoid
SE_PIN = 6    # PIN (PWM) for expiratory solenoid
PWM_O = None
PWM_I = None
PWM_E = None
pid = None


def load_pid_config():
    global pid
    with open('./pid.conf', 'r') as f:
        config = f.readline().split(',')
        pid.SetPoint = float(Variables.ps)
        pid.setKp(float(config[0]))
        pid.setKi(float(config[1]))
        pid.setKd(float(config[2]))


def create_pid_config():
    if not path.isfile('./pid.conf'):
        with open('./pid.conf', 'w') as f:
            f.write('%s,%s,%s' % (Variables.Kp, Variables.Ki, Variables.Kd))


def convert_pressure(p_hpa):
    """ returns inspiratory pressure relative to atm in cmH2O"""
    return (p_hpa * 1.0197442) - 1033.23


def init_parameters():
    global PWM_O, PWM_I, PWM_E, pid

    # Initialize PWM pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(SO_PIN, GPIO.OUT)
    GPIO.setup(SI_PIN, GPIO.OUT)
    # GPIO.setup(SE_PIN, GPIO.OUT)

    PWM_O = GPIO.PWM(SO_PIN, PWM_FREQ)
    PWM_I = GPIO.PWM(SI_PIN, PWM_FREQ)
    # PWM_E = GPIO.PWM(SE_PIN, PWM_FREQ)

    # Start the sensor reading service
    sensing_service = SensorReaderService()

    # Initialize PID controller
    create_pid_config()
    pid = PID(Variables.Kp, Variables.Ki, Variables.Kd)
    pid.SetPoint = Variables.ps
    pid.setSampleTime(Variables.pid_sampling_period)

    # Open all values
    PWM_O.ChangeDutyCycle(0)
    PWM_I.ChangeDutyCycle(100)
    # PWM_E.ChangeDutyCycle(0)    # Normally open, hence duty_ratio=0

###################################################################


init_parameters()

time.sleep(2)
print("P1 = %.1f,\tP2 = %.1f,\tP3 = %.1f,\tP4 = %.1f" % (Variables.p1, Variables.p2, Variables.p3, Variables.p4))

while True:
    # load the latest PID related config. [Kp, Ki, Kd]
    load_pid_config()

    # read pressure data
    pressure = Variables.p3

    if pressure is None:
        continue

    pid.update(convert_pressure(pressure))
    target_duty_ratio = pid.output
    target_duty_ratio = max(min(int(target_duty_ratio), 100), 0)

    # logger.debug("Target: %.1f | Current: %.1f | Duty Ratio: %d"
    #              % (Variables.ps, pressure, target_duty_ratio))
    print("Target: %.1f | Current: %.1f | Duty Ratio: %d" % (Variables.ps, convert_pressure(pressure), target_duty_ratio))

    # Set PWM to target duty
    PWM_I.ChangeDutyCycle(target_duty_ratio)

    time.sleep(Variables.pid_sampling_period - 0.005)
