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
SI_PIN = 12  # PIN (PWM) for inspiratory solenoid
SE_PIN = 14  # PIN (PWM) for expiratory solenoid
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
    global PWM_I, PWM_E, pid

    # Initialize PWM pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(SI_PIN, GPIO.OUT)
    GPIO.setup(SE_PIN, GPIO.OUT)
    PWM_I = GPIO.PWM(SI_PIN, PWM_FREQ)
    PWM_E = GPIO.PWM(SE_PIN, PWM_FREQ)

    # Start the sensor reading service
    sensing_service = SensorReaderService()

    # Initialize PID controller
    create_pid_config()
    pid = PID(Variables.Kp, Variables.Ki, Variables.Kd)
    pid.SetPoint = Variables.ps
    pid.setSampleTime(Variables.pid_sampling_period)


###################################################################


init_parameters()

while True:
    # load the latest PID related config. [Kp, Ki, Kd]
    load_pid_config()

    # read pressure data
    pressure = Variables.p3

    pid.update(convert_pressure(pressure))
    target_duty_ratio = pid.output
    target_duty_ratio = max(min(int(target_duty_ratio), 100), 0)

    print("Target: %.1f | Current: %.1f | Duty Ratio: %d" % (Variables.ps, convert_pressure(pressure), target_duty_ratio))

    # Set PWM to target duty
    PWM_I.ChangeDutyCycle(target_duty_ratio)

    time.sleep(Variables.pid_sampling_period - 0.005)
