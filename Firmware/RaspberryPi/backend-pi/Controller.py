# Controller v1.1
# 2020-05-09 12.05 AM (Melb)

# import os
import math
import time
from datetime import datetime
import threading
import RPi.GPIO as GPIO
import logging
import logging.config
from Variables import Variables
from SensorReader import SensorReader
from PWMController import PWMController
from MQTTTransceiver import MQTTTransceiver

# Internal parameters
T_IN = 2  # inspiratory time
T_EX = 3  # expiratory time
T_WT = 1  # waiting time

Pi = 2000  # peak inspiratory pressure in cmH2O
PEEP = 900  # PEEP
PWM_FREQ = 4  # frequency for PWM

# Constants
SI_PIN = 12  # PIN (PWM) for inspiratory solenoid
SE_PIN = 13  # PIN (PWM) for expiratory solenoid
INSP_FLOW = True
EXP_FLOW = False
DUTY_RATIO_100 = 100
DUTY_RATIO_0 = 0
NUMBER_OF_SENSORS = 4
BUS_1 = 1
BUS_2 = 3
BUS_3 = 4
BUS_4 = 5
INSP_PHASE = "inspiratory"
EXP_PHASE = "expiratory"
DISPLAY_TIME_AXIS = 0           # time axis value in display
DISPLAY_TIME_RANGE = 20   # the range of time axis in display

pressure_data = [0] * 6
PWM_I, PWM_E = None, None
threads_map = {}

mqtt = MQTTTransceiver()
Ki, Ke = 0, 0

# declare logger parameters
logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def thread_slice(pressure_data, index):
    sr = SensorReader(index)
    pressure = sr.read_pressure()
    pressure_data[index] = pressure


def read_data(phase=""):
    # read relevant pressure sensors from the smbus and return actual values
    threads = list()
    if phase == INSP_PHASE:
        for index in [BUS_1, BUS_2, BUS_3]:
            thread = threading.Thread(
                target=thread_slice, args=(pressure_data, index,))
            threads.append(thread)
            thread.start()
        for index, thread in enumerate(threads):
            thread.join()
        logger.debug("Pressure: P1[%.2f], P2[%.2f], P3[%.2f]" %
                     (pressure_data[BUS_1], pressure_data[BUS_2], pressure_data[BUS_3]))
        return pressure_data[BUS_1], pressure_data[BUS_2], pressure_data[BUS_3]
    elif phase == EXP_PHASE:
        for index in [BUS_3, BUS_4]:
            thread = threading.Thread(
                target=thread_slice, args=(pressure_data, index,))
            threads.append(thread)
            thread.start()
        for index, thread in enumerate(threads):
            thread.join()
        logger.debug("Pressure: P3[%.2f], P4[%.2f]" %
                     (pressure_data[BUS_3], pressure_data[BUS_4]))
        return pressure_data[BUS_3], pressure_data[BUS_4]
    else:
        for index in [BUS_1, BUS_2, BUS_3, BUS_4]:
            thread = threading.Thread(
                target=thread_slice, args=(pressure_data, index,))
            threads.append(thread)
            thread.start()
        for index, thread in enumerate(threads):
            thread.join()
        logger.debug("Pressure: P1[%.2f], P2[%.2f], P3[%.2f], P4[%.2f]" %
                     (pressure_data[BUS_1], pressure_data[BUS_2], pressure_data[BUS_3], pressure_data[BUS_4]))
        return pressure_data[BUS_1], pressure_data[BUS_2], pressure_data[BUS_3], pressure_data[BUS_4]


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
        p1, p2, p3, p4 = read_data()
        ki += calculate_k(p1, p2, flow_rate)
        ke += calculate_k(p3, p4, flow_rate)
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
    elif pin == SE_PIN:
        # Expiratory solenoid is normally OPEN. Hence flipping the duty ratio
        PWM_E.ChangeDutyCycle(DUTY_RATIO_100 - duty_ratio)

    logger.debug("Changed duty cycle to " +
                 str(duty_ratio) + " on pin " + str(pin))


# def control_solenoid(pin, duty_ratio):
#     """ emulate pwm on a digital out pin """
#     logger.info("Entering control_solenoid()...")
#     on_time = PWM_PERIOD * duty_ratio
#     off_time = PWM_PERIOD * (1 - duty_ratio)
#
#     if pin in threads_map:
#         threads_map[pin].stop()
#         threads_map[pin].join()
#
#     t = PWMController(datetime.now().strftime('%Y%m%d%H%M%S%f'), pin, on_time, off_time)
#     threads_map[pin] = t
#
#     # Don't want these threads to run when the main program is terminated
#     t.daemon = True
#     t.start()
#
#     logger.info("Leaving control_solenoid().")


def get_average_flow_rate_and_pressure(is_insp_phase):
    """ read p1 and p2 over 200 milliseconds and return average volume rate """

    nSamples = 4  # average over 4 samples
    delay = 0.05  # 50 milliseconds
    n, p, q = 0, 0, 0

    # Take the average over 'nSamples' pressure readings, 'delay' seconds apart to calculate flow rate
    while n < nSamples:
        if is_insp_phase:
            p1, p2, p3 = read_data(INSP_PHASE)  # pressures
            q += Ki * math.sqrt(abs(p1 - p2))  # flow rate
        else:
            p3, p4 = read_data(EXP_PHASE)  # pressures
            q += Ke * math.sqrt(abs(p3 - p4))  # flow rate

        p += p3

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


def send_to_display(delta_t, pressure, flow_rate, volume):
    """ send the given parameters to display unit via mqtt """

    global DISPLAY_TIME_AXIS

    # Recalculate the time axis value to fit in the graph
    DISPLAY_TIME_AXIS += delta_t
    DISPLAY_TIME_AXIS %= DISPLAY_TIME_RANGE

    mqtt.sender(mqtt.PRESSURE_TOPIC, convert_pressure(pressure))
    mqtt.sender(mqtt.FLOWRATE_TOPIC, flow_rate)
    mqtt.sender(mqtt.VOLUME_TOPIC, volume)
    # TODO: send also time with each topic so that it can be graphed based on time
    logger.debug("[ %.1f sec ] : Pressure: %.2f L, Flow rate: %.2f L/min, Volume: %.2f L,  "
                 % (round(DISPLAY_TIME_AXIS, 2), convert_pressure(pressure), flow_rate, volume))


def insp_phase(demo_level):
    """ inspiratory phase tasks
        demo_level is a temporary hack to introduce two flow rate levels until pid controller is implemented """

    # os.system('play -nq -t alsa synth {} sine {}'.format(1, 440))

    logger.info("Entering inspiratory phase...")
    start_time = datetime.now()
    t1, t2 = start_time, start_time
    ti = 0  # instantaneous time
    q1, q2 = 0, 0  # flow rates
    vi = 0  # volume
    solenoids_closed = False

    # Control solenoids
    control_solenoid(SI_PIN, DUTY_RATIO_100)
    control_solenoid(SE_PIN, DUTY_RATIO_0)

    while ti < T_IN:

        t1 = t2
        q1 = q2
        q2, p3 = get_average_flow_rate_and_pressure(INSP_FLOW)
        t2 = datetime.now()

        if vi > Variables.vt:
            if not solenoids_closed:
                # Tidal volume has reached, CLOSE all solonoids
                control_solenoid(SI_PIN, DUTY_RATIO_0)
                control_solenoid(SE_PIN, DUTY_RATIO_0)
                solenoids_closed = True

            ti = (t2 - start_time).total_seconds()
            delta_t = (t2 - t1).total_seconds()
            send_to_display(delta_t, p3, 0, vi)          # flow rate is 0 when insp. solenoid is closed
            continue

        # Calculate volume
        vi += (q1 + q2) / 2 * (t2 - t1).total_seconds() / 60

        di = calculate_pid_duty_ratio(demo_level)
        control_solenoid(SI_PIN, di)

        ti = (t2 - start_time).total_seconds()
        delta_t = (t2 - t1).total_seconds()
        send_to_display(delta_t, p3, q2, vi)

        logger.debug("fio2: %.2f, vt: %.2f, ie: %.2f, rr: %.2f, peep: %.2f" % (
            Variables.fio2, Variables.vt, Variables.ie_e, Variables.rr, Variables.peep))

    logger.info("Leaving inspiratory phase.")


def exp_phase():
    """ expiratory phase tasks """
    logger.info("Entering expiratory phase...")
    start_time = datetime.now()
    t1, t2 = start_time, start_time
    ti = 0
    q1, q2 = 0, 0
    vi = 0

    control_solenoid(SI_PIN, DUTY_RATIO_0)
    control_solenoid(SE_PIN, DUTY_RATIO_100)

    while ti < T_EX:
        t1 = t2
        q1 = q2
        q2, p3 = get_average_flow_rate_and_pressure(EXP_FLOW)
        t2 = datetime.now()

        # Calculate volume
        vi += (q1 + q2) / 2 * (t2 - t1).total_seconds() / 60

        ti = (t2 - start_time).total_seconds()
        delta_t = (t2 - t1).total_seconds()
        send_to_display(delta_t, p3, (-1 * q2), vi)

    logger.info("<< CHART >> Actual tidal volume delivered : %.3f L " % vi)
    # mqtt.sender(mqtt.ACTUAL_TIDAL_VOLUME_TOPIC, vi)

    logger.info("Leaving expiratory phase.")


def wait_phase():
    """ waiting phase tasks """
    logger.info("Entering wait phase...")
    control_solenoid(SI_PIN, DUTY_RATIO_0)
    control_solenoid(SE_PIN, DUTY_RATIO_0)
    time.sleep(T_WT)
    logger.info("Leaving wait phase.")


def convert_pressure(p_hpa):
    """ returns inspiratory pressure in cmH2O"""
    return p_hpa * 1.0197442


def calc_respiratory_params():
    """ calculate inspiratory time and expiratory time using parameters set via UI """
    global T_IN, T_EX
    one_breath_time = 60 / Variables.rr
    T_IN = one_breath_time * Variables.ie_i / (Variables.ie_i + Variables.ie_e)
    T_EX = one_breath_time * Variables.ie_e / (Variables.ie_i + Variables.ie_e)


# Initialize the parameters
def init_parameters():
    global PWM_I, PWM_E

    # Initialize digital output pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(SI_PIN, GPIO.OUT)
    GPIO.setup(SE_PIN, GPIO.OUT)

    PWM_I = GPIO.PWM(SI_PIN, PWM_FREQ)
    PWM_E = GPIO.PWM(SE_PIN, PWM_FREQ)

    calc_respiratory_params()


#######################################################################################################

try:
    init_parameters()

    # 12 here is the intended flow_rate for calibration in L/min
    Ki, Ke = calibrate_flow_meter(12)

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
