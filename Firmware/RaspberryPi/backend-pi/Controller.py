import os
import math
import json
import time
from datetime import datetime
import threading
import RPi.GPIO as GPIO
import logging
import logging.config
from Variables import Variables
# from SensorReader import SensorReader
from SensorReaderService import SensorReaderService
# from PWMController import PWMController
from MQTTTransceiver import MQTTTransceiver

# Internal parameters
T_IN = 2  # inspiratory time
T_EX = 3  # expiratory time
T_WT = 1  # waiting time

Pi = 2000  # peak inspiratory pressure in cmH2O
PWM_FREQ = 2  # frequency for PWM

# Constants
SI_PIN = 12  # PIN (PWM) for inspiratory solenoid
SE_PIN = 13  # PIN (PWM) for expiratory solenoid
INSP_FLOW = True
EXP_FLOW = False
DUTY_RATIO_100 = 100
DUTY_RATIO_0 = 0
INSP_TOTAL_VOLUME = 0   # total inspiratory volume delivered

pressure_data = [0] * 6
PWM_I, PWM_E = None, None

mqtt = None
sensing_service = None
Ki, Ke = 0, 0
TIME_REF_MINUTE_VOL = None
MINUTE_VOLUME = 0

# declare logger parameters
logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def calculate_k(p1, p2, flow_rate):
    return flow_rate / math.sqrt(abs(p1 - p2))


# With current settings flow meter will be calibrated over 5 seconds (nSamples * delay)
def calibrate_flow_meter(flow_rate):
    """ returns the calibrated k for both insp and exp flow meters, calculated based on multiple pressure readings """

    # Turn ON both the solenoids fully for calibration
    PWM_I.start(DUTY_RATIO_100)
    PWM_E.start(DUTY_RATIO_100)

    # Introduce a delay to achieve a stable flow across the flow meters
    time.sleep(2)

    nSamples = 10  # average over 10 samples
    delay = 0.5  # 0.5 seconds
    n = 0
    ki = 0
    ke = 0
    # Take the average over 'nSamples' pressure readings, 'delay' seconds apart to calculate k
    while n < nSamples:
        ki += calculate_k(Variables.p1, Variables.p2, flow_rate)
        ke += calculate_k(Variables.p3, Variables.p4, flow_rate)
        n += 1
        time.sleep(delay)

    ki /= nSamples
    ke /= nSamples
    logger.debug(
        "Flow meter was calibrated. k_ins = %.4f, k_exp = %.4f" % (ki, ke))
    return ki, ke


def control_solenoid(pin, duty_ratio):
    if pin == SI_PIN:
        PWM_I.ChangeDutyCycle(duty_ratio)
        logger.debug("Changed duty cycle to " + str(duty_ratio) + " on pin " + str(pin))
    elif pin == SE_PIN:
        logger.debug("Changed duty cycle to " + str(DUTY_RATIO_100 - duty_ratio) + " on pin " + str(pin))
        # Expiratory solenoid is normally OPEN. Hence flipping the duty ratio
        PWM_E.ChangeDutyCycle(DUTY_RATIO_100 - duty_ratio)


def get_average_flow_rate_and_pressure(is_insp_phase):
    """ read p1 and p2 over 200 milliseconds and return average volume rate """

    nSamples = 4  # average over 4 samples
    delay = 0.05  # 50 milliseconds
    n, p, q = 0, 0, 0

    # Take the average over 'nSamples' pressure readings, 'delay' seconds apart to calculate flow rate
    while n < nSamples:
        if is_insp_phase:
            q += Ki * math.sqrt(abs(Variables.p1 - Variables.p2))  # flow rate
        else:
            q += Ke * math.sqrt(abs(Variables.p3 - Variables.p4))  # flow rate

        p += Variables.p3

        n += 1
        time.sleep(delay)

    return q / nSamples, p / nSamples


def calculate_pid_duty_ratio(demo_level):
    """ TODO: implement the PID controller to determine the required duty ratio to achieve the desired pressure curve
        Currently a temporary hack is implemented with demo_level """
    duty_ratio = 100
    if demo_level == 1:
        duty_ratio = 20

    return duty_ratio


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

    payload = create_chart_payload(timeT, convert_pressure(pressure), flow_rate, volume)
    mqtt.sender(mqtt.CHART_DATA_TOPIC, payload)
    logger.debug(payload)


def insp_phase(demo_level):
    """ inspiratory phase tasks
        demo_level is a temporary hack to introduce two flow rate levels until pid controller is implemented """

    global INSP_TOTAL_VOLUME, TIME_REF_MINUTE_VOL
    logger.info("Entering inspiratory phase...")

    # beep sound added to inspiratory cycle
    os.system("echo -ne '\007'")

    start_time = datetime.now()
    t1, t2 = start_time, start_time
    ti = 0  # instantaneous time
    q1, q2 = 0, 0  # flow rates
    vi = 0  # volume
    pip = 0 # peak inspiratory pressure
    solenoids_closed = False

    # Control solenoids
    control_solenoid(SI_PIN, DUTY_RATIO_100)
    control_solenoid(SE_PIN, DUTY_RATIO_0)

    while ti < T_IN:

        t1 = t2
        q1 = q2
        q2, p3 = get_average_flow_rate_and_pressure(INSP_FLOW)
        t2 = datetime.now()

        # Record peak inspiratory pressure (pip)
        if p3 > pip:
            pip = p3

        if vi > Variables.vt:
            if not solenoids_closed:
                # Tidal volume has reached, CLOSE all solonoids
                control_solenoid(SI_PIN, DUTY_RATIO_0)
                control_solenoid(SE_PIN, DUTY_RATIO_0)
                solenoids_closed = True

            ti = (t2 - start_time).total_seconds()
            send_to_display(t2, p3, 0, vi)  # flow rate is 0 when insp. solenoid is closed
            continue

        # Calculate volume in milli-litres
        vi += 1000 * (q1 + q2) / 2 * (t2 - t1).total_seconds() / 60

        # If a minute has elapsed, submit the MINUTE_VOLUME to display
        if TIME_REF_MINUTE_VOL is not None and (t2 - TIME_REF_MINUTE_VOL).total_seconds() > 60:
            submit_minute_vol(t2)

        di = calculate_pid_duty_ratio(demo_level)
        control_solenoid(SI_PIN, di)

        ti = (t2 - start_time).total_seconds()
        send_to_display(t2, p3, q2, vi)

        logger.debug("fio2: %.2f, vt: %.2f, ie: %.2f, rr: %.2f, peep: %.2f" % (
            Variables.fio2, Variables.vt, Variables.ie, Variables.rr, Variables.peep))

    # Store tidal volume for expiratory phase net volume calculation
    INSP_TOTAL_VOLUME = vi

    # Send pip to GUI
    mqtt.sender(mqtt.PIP_TOPIC, pip)
    logger.info("[%.4f] Pip is : %.3f mL " % (ti, pip))

    logger.info("Leaving inspiratory phase.")


def exp_phase():
    """ expiratory phase tasks """
    logger.info("Entering expiratory phase...")

    global INSP_TOTAL_VOLUME, TIME_REF_MINUTE_VOL, MINUTE_VOLUME
    start_time = datetime.now()
    t1, t2 = start_time, start_time
    ti = 0
    q1, q2 = 0, 0
    vi = 0

    control_solenoid(SI_PIN, DUTY_RATIO_0)
    control_solenoid(SE_PIN, DUTY_RATIO_100)

    # Start calculating minute volume
    if TIME_REF_MINUTE_VOL is None:
        TIME_REF_MINUTE_VOL = start_time

    while ti < T_EX:
        t1 = t2
        q1 = q2
        q2, p3 = get_average_flow_rate_and_pressure(EXP_FLOW)
        t2 = datetime.now()

        # Calculate volume
        vi += 1000 * (q1 + q2) / 2 * (t2 - t1).total_seconds() / 60
        ti = (t2 - start_time).total_seconds()

        # Handle minute volume calculations
        if (t2 - TIME_REF_MINUTE_VOL).total_seconds() < 60:
            MINUTE_VOLUME += vi
        else:
            submit_minute_vol(t2)

        send_to_display(t2, p3, (-1 * q2), (INSP_TOTAL_VOLUME - vi))
        logger.debug("ti = %.4f,     T_EX = %.4f" % (ti, T_EX))

    logger.info("<< CHART >> Actual tidal volume delivered : %.3f mL " % vi)
    mqtt.sender(mqtt.ACTUAL_TIDAL_VOLUME_TOPIC, vi)
    INSP_TOTAL_VOLUME = 0
    logger.info("Leaving expiratory phase.")


def submit_minute_vol(reset_time):
    global TIME_REF_MINUTE_VOL, MINUTE_VOLUME

    # Send minute volume to GUI
    mqtt.sender(mqtt.MINUTE_VOLUME_TOPIC, round(MINUTE_VOLUME, 2))

    # Reset minute volume calculation
    TIME_REF_MINUTE_VOL = reset_time
    MINUTE_VOLUME = 0


def wait_phase():
    """ waiting phase tasks """
    logger.info("Entering wait phase...")
    control_solenoid(SI_PIN, DUTY_RATIO_0)
    control_solenoid(SE_PIN, DUTY_RATIO_0)
    time.sleep(T_WT)
    logger.info("Leaving wait phase.")


def convert_pressure(p_hpa):
    """ returns inspiratory pressure relative to atm in cmH2O"""
    return (p_hpa * 1.0197442) - 1033.23


def calc_respiratory_params():
    """ calculate inspiratory time and expiratory time using parameters set via UI """
    global T_IN, T_EX
    one_breath_time = 60 / Variables.rr
    T_IN = one_breath_time * 1 / (1 + Variables.ie)
    T_EX = one_breath_time * Variables.ie / (1 + Variables.ie)


# Initialize the parameters
def init_parameters():
    global PWM_I, PWM_E, sensing_service, mqtt

    # Initialize PWM pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(SI_PIN, GPIO.OUT)
    GPIO.setup(SE_PIN, GPIO.OUT)

    PWM_I = GPIO.PWM(SI_PIN, PWM_FREQ)
    PWM_E = GPIO.PWM(SE_PIN, PWM_FREQ)

    # Start the sensor reading service
    sensing_service = SensorReaderService()

    # Start the MQTT transceiver to communicate with GUI
    mqtt = MQTTTransceiver()

    calc_respiratory_params()


#######################################################################################################

try:
    init_parameters()

    # Calibration should start after a trigger from user with a valid flow rate
    while Variables.calib_flow_rate < 0:
        time.sleep(2)

    # Calibrate the flow meter
    Ki, Ke = calibrate_flow_meter(Variables.calib_flow_rate)

    while True:
        # slow flow rate
        # logger.info("***** Slower flow rate cycle *****")
        # insp_phase(1)
        # exp_phase()
        # wait_phase()
        # logger.info("***** Slower cycle end *****")

        # faster flow rate
        logger.info("***** Faster flow rate cycle *****")
        insp_phase(2)
        exp_phase()
        # wait_phase()
        logger.info("***** Faster cycle end *****")

        # use the latest input parameters set via UI
        calc_respiratory_params()

finally:
    mqtt.clean_up()
    # Set the solenoids to desired states before exiting
    PWM_I.start(DUTY_RATIO_100)
    PWM_E.start(DUTY_RATIO_100)
    print("\nInspiratory and expiratory solenoids were reset before exiting. Good bye...\n")
