import sys

sys.path.append('..')

from PID import PID
from SensorReaderService import SensorReaderService
from MQTTTransceiver import MQTTTransceiver
from Variables import Variables
from datetime import datetime
import time
import json
from os import path
import RPi.GPIO as GPIO

# Constants
SO_PIN = 13  # PIN (PWM) for O2 intake solenoid
SI_PIN = 12  # PIN (PWM) for inspiratory solenoid
SE_PIN = 6  # PIN (PWM) for expiratory solenoid
PWM_O = None
PWM_I = None
PWM_E = None
pid = None

Ti = 4
Te = 10
leak_duty = 13

mqtt = None


def load_pid_config():
    global pid
    with open('./pid.conf', 'r') as f:
        config = f.readline().split(',')
        pid.SetPoint = float(Variables.pip_target)
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
    global PWM_O, PWM_I, pid, mqtt

    # Initialize PWM pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(SO_PIN, GPIO.OUT)
    GPIO.setup(SI_PIN, GPIO.OUT)
    GPIO.setup(SE_PIN, GPIO.OUT)

    PWM_O = GPIO.PWM(SO_PIN, Variables.PWM_FREQ)
    PWM_I = GPIO.PWM(SI_PIN, Variables.PWM_FREQ)

    # Start the sensor reading service
    sensing_service = SensorReaderService()

    # Initialize PID controller
    create_pid_config()
    pid = PID(Variables.Kp, Variables.Ki, Variables.Kd)
    pid.SetPoint = Variables.pip_target
    pid.setSampleTime(Variables.pid_sampling_period)

    # Open all solenoids
    PWM_O.start(0)
    PWM_I.start(100)
    GPIO.output(SE_PIN, GPIO.LOW)  # Normally open, hence GPIO.LOW
    # PWM_O.ChangeDutyCycle(0)
    # PWM_I.ChangeDutyCycle(100)

    # Start the MQTT transceiver to communicate with GUI
    mqtt = MQTTTransceiver()



def create_chart_payload(t, pressure, flow_rate, volume):
    payload = {
        'time': t.isoformat(),
        'pressure': round(pressure, 2),
        'flow_rate': round(flow_rate, 2),
        'volume': round(volume, 2)
    }
    return json.dumps(payload)


def send_to_display(timeT, pressure, flow_rate, volume):
    """ send the given parameters to display unit via mqtt """

    payload = create_chart_payload(timeT, pressure, flow_rate, volume)
    mqtt.sender(mqtt.CHART_DATA_TOPIC, payload)

###################################################################


def insp_phase():

    # set solenoids
    GPIO.output(SE_PIN, GPIO.HIGH)
    time.sleep(0.1)

    print("\n=== INSP ===")

    # load the latest PID related config. [Kp, Ki, Kd]
    load_pid_config()
    start_time = datetime.now()
    t1 = start_time
    t = 0
    peak_pressure = 0
    skip_pid = False

    while t < Ti:
        # read pressure data
        pressure = Variables.p3

        if pressure is None:
            continue

        send_to_display(t1, convert_pressure(pressure), 0, 0)

        if pressure > peak_pressure:
            peak_pressure = pressure

        if (convert_pressure(pressure) > (Variables.pip_target - 1)) or skip_pid:
            PWM_I.ChangeDutyCycle(leak_duty)
            t1 = datetime.now()
            t = (t1 - start_time).total_seconds()
            print(">>> Target: %.1f | Current: %.1f | Duty Ratio: %d" % (Variables.pip_target, convert_pressure(pressure), leak_duty))
            skip_pid = True
            time.sleep(Variables.pid_sampling_period)
            continue

        pid.update(convert_pressure(pressure))
        target_duty_ratio = pid.output
        target_duty_ratio = max(min(int(target_duty_ratio), 100), 0)

        # logger.debug("Target: %.1f | Current: %.1f | Duty Ratio: %d"
        #              % (Variables.pip_target, pressure, target_duty_ratio))
        print(
            "Target: %.1f | Current: %.1f | Duty Ratio: %d" % (Variables.pip_target, convert_pressure(pressure), target_duty_ratio))

        # Set PWM to target duty
        PWM_I.ChangeDutyCycle(target_duty_ratio)

        time.sleep(Variables.pid_sampling_period)
        t1 = datetime.now()
        t = (t1 - start_time).total_seconds()

    print("Max P = %.1f" % convert_pressure(peak_pressure))


def exp_phase():

    # set solenoids
    PWM_I.ChangeDutyCycle(0)
    GPIO.output(SE_PIN, GPIO.LOW)
    time.sleep(0.1)

    print("\n=== EXP ===")

    start_time = datetime.now()
    t1 = start_time
    t = 0

    while t < Te:
        # read pressure data
        pressure = Variables.p3

        if pressure is None:
            continue

        send_to_display(t1, convert_pressure(pressure), 0, 0)
        print("Pressure = %.1f" % convert_pressure(pressure))
        time.sleep(Variables.pid_sampling_period)
        t1 = datetime.now()
        t = (t1 - start_time).total_seconds()


try:

    init_parameters()

    time.sleep(2)
    print("P1 = %.1f,\tP2 = %.1f,\tP3 = %.1f,\tP4 = %.1f" % (Variables.p1, Variables.p2, Variables.p3, Variables.p4))

    while True:
        insp_phase()
        exp_phase()

finally:
    # Set the solenoids to desired states before exiting
    PWM_O.ChangeDutyCycle(0)
    PWM_I.ChangeDutyCycle(0)
    GPIO.output(SE_PIN, GPIO.LOW)  # Normally open, hence GPIO.LOW
    time.sleep(2)
