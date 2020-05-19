from PID import PID
from ..SensorReaderService import SensorReaderService
from ..Variables import Variables
import time
import RPi.GPIO as GPIO

# Constants
PWM_FREQ = 2  # frequency for PWM
SI_PIN = 12  # PIN (PWM) for inspiratory solenoid
PWM_I = None

Psupport = 10
P = 10
I = 1
D = 1
sampling_time = 0.5

pid = PID(P, I, D)
pid.SetPoint = Psupport
pid.setSampleTime(sampling_time)

# count = 0
# pressureArray = [0, 1, 4, 7, 9, 7, 6, 5, 7, 8, 10, 10]
#
#
# def readPressure():
#     return pressureArray[count]


def init_parameters():
    global PWM_I

    # Initialize PWM pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(SI_PIN, GPIO.OUT)

    PWM_I = GPIO.PWM(SI_PIN, PWM_FREQ)

    # Start the sensor reading service
    sensing_service = SensorReaderService()


while True:
    # read pressure data
    pressure = Variables.p3

    pid.update(pressure)
    target_duty_ratio = pid.output
    target_duty_ratio = max(min(int(target_duty_ratio), 100), 0)

    print("Target: %.1f | Current: %.1f | Duty Ratio: %s %%" % (Psupport, pressure, target_duty_ratio))

    # Set PWM to target duty
    PWM_I.ChangeDutyCycle(target_duty_ratio)

    time.sleep(sampling_time - 0.005)
