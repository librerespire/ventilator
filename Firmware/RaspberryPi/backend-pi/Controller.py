# Controller v1.1
# 2020-05-09 12.05 AM (Melb)

import math
import time
from datetime import datetime
import threading
import RPi.GPIO as GPIO
from SensorReader import SensorReader
from PWMController import PWMController
import logging
import logging.config

# Parameters
Ti = 5  # inspiratory time
Te = 5  # expiratory time
Tw = 1  # waiting time
Vt = 5  # tidal volume
Pi = 2000  # peak inspiratory pressure in cmH2O
Peep = 900
PWM_PERIOD = 2  # time period for PWM

# Constants
SI_PIN = 20  # PIN number for inspiratory solenoid
SE_PIN = 21  # PIN number for expiratory solenoid
DUTY_RATIO_100 = 1
DUTY_RATIO_0 = 0
NUMBER_OF_SENSORS = 4
BUS_1 = 1
BUS_2 = 3
BUS_3 = 4
BUS_4 = 5

pressure_data = [0] * 6
threads_map = {}

# declare logger parameters
logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def thread_slice(pressure_data, index):
    sr = SensorReader(index)
    pressure = sr.read_pressure()
    pressure_data[index] = pressure


def read_data():
    # read four pressure sensors from the smbus and return actual values
    threads = list()
    for index in [BUS_1, BUS_2, BUS_3, BUS_4]:
        thread = threading.Thread(target=thread_slice, args=(pressure_data, index,))
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
    control_solenoid(SI_PIN, DUTY_RATIO_100)
    control_solenoid(SE_PIN, DUTY_RATIO_100)

    nSamples = 10  # average over 10 samples
    delay = 0.005  # 0.5 seconds
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
    logger.debug("Flow meter was calibrated. k_ins = %.4f, k_exp = %.4f" % (ki, ke))
    return ki, ke


def control_solenoid(pin, duty_ratio):
    # read four pressure sensors from the smbus and return actual values
    logger.info("Entering control_solenoid()...")
    on_time = PWM_PERIOD * duty_ratio
    off_time = PWM_PERIOD * (1 - duty_ratio)

    if pin in threads_map:
        threads_map[pin].stop()
        threads_map[pin].join()

    t = PWMController(datetime.now().strftime('%Y%m%d%H%M%S%f'), pin, on_time, off_time)
    threads_map[pin] = t

    # Don't want these threads to run when the main program is terminated
    t.daemon = True
    t.start()

    logger.info("Leaving control_solenoid().")


def get_average_volume_rate(is_insp_phase):
    """ read p1 and p2 over 200 milliseconds and return average volume rate """

    nSamples = 4  # average over 4 samples
    delay = 0.005  # 50 milliseconds
    n = 0
    q = 0
    # Take the average over 'nSamples' pressure readings, 'delay' seconds apart to calculate flow rate
    while n < nSamples:
        p1, p2, p3, p4 = read_data()
        if is_insp_phase:
            q += Ki * math.sqrt(abs(p1 - p2))
        else:
            q += Ke * math.sqrt(abs(p3 - p4))

        n += 1
        time.sleep(delay)

    return q / nSamples


def calculate_pid_duty_ratio(demo_level):
    """ TODO: implement the PID controller to determine the required duty ratio to achieve the desired pressure curve
        Currently a temporary hack is implemented with demo_level """
    duty_ratio = 0.8
    if demo_level == 1:
        duty_ratio = 0.2

    return duty_ratio


def insp_phase(demo_level):
    """ inspiratory phase tasks
        demo_level is a temporary hack to introduce two flow rate levels until pid controller is implemented """

    logger.info("Entering inspiratory phase...")
    start_time = datetime.now()
    t1, t2 = start_time, start_time
    ti = 0
    q1, q2 = 0, 0
    vi = 0

    # Control solenoids
    control_solenoid(SE_PIN, DUTY_RATIO_0)

    while ti < Ti and vi < Vt:
        t1 = t2
        q1 = q2
        q2 = get_average_volume_rate(True)
        t2 = datetime.now()

        vi += (q1 + q2) / 2 * (t2 - t1).total_seconds() / 60

        di = calculate_pid_duty_ratio(demo_level)
        control_solenoid(SI_PIN, di)

        ti = (datetime.now() - start_time).total_seconds()
        logger.info("Flow rate: %.2f VI: %.2f TI: %.2f" % (q2, vi, ti))

    logger.info("Leaving inspiratory phase.")


def exp_phase():
    """ expiratory phase tasks """
    logger.info("Entering expiratory phase...")
    start_time = datetime.now()
    t1, t2 = start_time, start_time
    ti = 0
    q1, q2 = 0, 0
    vi = 0
    p3 = Peep

    control_solenoid(SI_PIN, DUTY_RATIO_0)
    control_solenoid(SE_PIN, DUTY_RATIO_100)

    while ti < Te and p3 <= Peep:
        t1 = t2
        q1 = q2
        q2 = get_average_volume_rate(False)
        t2 = datetime.now()

        vi += (q1 + q2) / 2 * (t2 - t1).total_seconds() / 60

        p1, p2, p3, p4 = read_data()
        if p3 < Peep:
            control_solenoid(SE_PIN, 0)

        ti = (datetime.now() - start_time).total_seconds()
        logger.info(q2, vi, p3, ti)

    logger.info("Leaving expiratory phase.")
    logger.info("Actual tidal volume delivered : %.3f L " % vi)


def wait_phase():
    """ waiting phase tasks """
    logger.info("Entering wait phase...")
    control_solenoid(SI_PIN, DUTY_RATIO_0)
    control_solenoid(SE_PIN, DUTY_RATIO_0)
    time.sleep(Tw)
    logger.info("Leaving wait phase.")


def convert_pressure(p_hpa):
    """ returns inspiratory pressure in cmH2O"""
    return p_hpa * 1.0197442


#######################################################################################################

# Initialize digital output pins
GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
GPIO.setup(SI_PIN, GPIO.OUT)
GPIO.setup(SE_PIN, GPIO.OUT)

# 12 here is the intended flow_rate for calibration in L/min
Ki, Ke = calibrate_flow_meter(12)

while True:
    # slow flow rate
    logger.info("***** Slower flow rate cycle *****")
    insp_phase(1)
    exp_phase()
    wait_phase()
    logger.info("***** Slower cycle end *****")

    # faster flow rate
    # logger.info("***** Faster flow rate cycle *****")
    # insp_phase(2)
    # exp_phase()
    # wait_phase()
    # logger.info("***** Faster cycle end *****")
