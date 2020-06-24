from os import path, system
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
from PID import PID
from Alarm import AlarmManager, AlarmType, AlarmLevel


# Internal parameters
T_IN = 2  # inspiratory time
T_EX = 3  # expiratory time
T_WT = 1  # waiting time

PWM_FREQ = 2  # frequency for PWM
pid = None

# Constants
SI_PIN = 12  # PIN (PWM) for inspiratory solenoid
SO_PIN = 13  # PIN 6 used for medical air valve
SE_PIN = 6  # PIN (PWM) for expiratory solenoid
INSP_FLOW = True
EXP_FLOW = False
DUTY_RATIO_100 = 100
DUTY_RATIO_0 = 0
INSP_TOTAL_VOLUME = 0  # total inspiratory volume delivered
PWM_I, PWM_O = None, None

# Last pressure data
last_p1 = 0;
last_p2 = 0;
last_p3 = 0;
last_p4 = 0;

mqtt = None
alarms = None
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

    # Turn ON all three solenoids fully for calibration
    PWM_I.start(DUTY_RATIO_100)
    PWM_O.start(DUTY_RATIO_100)
    control_solenoid(SE_PIN, DUTY_RATIO_100)

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
    logger.debug("Flow meter was calibrated. k_ins = %.4f, k_exp = %.4f\n Latest pressure readings are,"
                 "\nP1=%.2f,\nP2=%.2f,\nP3=%.2f,\nP4=%.2f,\n" % (
                     ki, ke, Variables.p1, Variables.p2, Variables.p3, Variables.p4))
    return ki, ke


def control_solenoid(pin, duty_ratio):
    if pin == SI_PIN:
        PWM_I.ChangeDutyCycle(duty_ratio)
        logger.debug("Changed duty cycle to " + str(duty_ratio) + " on pin " + str(pin))
    elif pin == SO_PIN:
        PWM_O.ChangeDutyCycle(duty_ratio)
        logger.debug("Changed duty cycle to " + str(duty_ratio) + " on pin " + str(pin))
    elif pin == SE_PIN:
        # Oxygen solenoid is normally OPEN. Hence flipping the duty ratio
        level = GPIO.HIGH
        if duty_ratio == DUTY_RATIO_100:
            level = GPIO.LOW
        logger.debug("Changed duty cycle to " + str(level) + " on pin " + str(pin))
        GPIO.output(SE_PIN, level)


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


def calculate_pid_duty_ratio(pressure):
    """ PID controller determines the required duty ratio to achieve the desired pressure curve """

    # TODO: Calculate duty ratio for medical air and oxygen separately
    logger.debug("<<<< HIT PID Controller >>>> : pressure = " + str(pressure))
    pid.update(pressure)
    duty_ratio = pid.output

    # Duty ratio is adjusted between 0 and 100
    duty_ratio = max(min(int(duty_ratio), 100), 0)

    logger.debug("<<<< LEAVE PID Controller >>>> : duty_ratio = " + str(duty_ratio))

    # Currently both the medical air and oxygen are using the same duty ratio
    return duty_ratio, duty_ratio


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
    logger.debug(payload)


def insp_phase():
    """ inspiratory phase tasks """

    global INSP_TOTAL_VOLUME, TIME_REF_MINUTE_VOL
    logger.info("Entering inspiratory phase...")

    # beep sound added to inspiratory cycle
    system("echo -ne '\007'")

    # Control solenoids
    control_solenoid(SI_PIN, DUTY_RATIO_100)
    control_solenoid(SO_PIN, DUTY_RATIO_100)
    control_solenoid(SE_PIN, DUTY_RATIO_0)

    start_time = datetime.now()
    t1, t2 = start_time, start_time
    ti = 0  # instantaneous time
    q1, q2 = 0, 0  # flow rates
    vi = 0  # volume
    pip = 0  # peak inspiratory pressure
    solenoids_closed = False
    only_exp_sol_open = False
    p_control_mode = Variables.mode is Variables.P_CONTROL    # ventilator in pressure control mode

    # Reset inspiratory cycle volume
    INSP_TOTAL_VOLUME = 0

    while ti < T_IN:

        send_pressure_data()

        t1 = t2
        q1 = q2
        q2, p3 = get_average_flow_rate_and_pressure(INSP_FLOW)
        t2 = datetime.now()

        # Record peak inspiratory pressure (pip)
        if p3 > pip:
            pip = p3

        # if safety pressure limit has reached, close all solenoids except exp to release pressure quickly
        if p_control_mode and (p3 > Variables.pmax):
            if not only_exp_sol_open:
                control_solenoid(SI_PIN, DUTY_RATIO_0)
                control_solenoid(SO_PIN, DUTY_RATIO_0)
                control_solenoid(SE_PIN, DUTY_RATIO_100)
                time.sleep(0.1)
                only_exp_sol_open = True

            # raise an alarm
            alarms.raise_alarm(AlarmType.PMAX_REACHED, AlarmLevel.MAJOR,
                               "Current pressure (%.1f) has exceeded Pmax (%.1f)" % (p3, Variables.pmax))
            ti = (t2 - start_time).total_seconds()
            send_to_display(t2, p3, 0, vi)  # flow rate is 0 when insp. solenoid is closed
            continue
        elif p_control_mode and (p3 < Variables.pmax):
            # p3 is below Pmax, clear the alarm
            alarms.clear_alarm(AlarmType.PMAX_REACHED,
                               "Current pressure (%.1f) has dropped below Pmax (%.1f)" % (p3, Variables.pmax))

        # if pressure is beyond the target threshold (15% above target), rely on PID controller to bring it down
        # However, need to raise an alarm
        if p_control_mode and (p3 > Variables.pip_target * 1.15):
            # raise an alarm
            alarms.raise_alarm(AlarmType.PIP_REACHED, AlarmLevel.MINOR,
                               "Current pressure (%.1f) has exceeded Pip (%.1f)" % (p3, Variables.pip_target))
        elif p_control_mode and (p3 < Variables.pip_target * 1.15):
            # p3 is dropped down to targeted pip, clear teh alarm
            alarms.clear_alarm(AlarmType.PIP_REACHED,
                               "Current pressure (%.1f) has dropped below pip (%.1f)" % (p3, Variables.pip_target))

        # Operating in volume control mode, and tidal volume has reached, CLOSE all solonoids
        if not p_control_mode and (vi > Variables.vt):
            if not solenoids_closed:
                close_all_solenoids(0.1)
                solenoids_closed = True

            ti = (t2 - start_time).total_seconds()
            send_to_display(t2, p3, 0, vi)  # flow rate is 0 when insp. solenoid is closed
            continue

        # Calculate volume in milli-litres
        vi += 1000 * (q1 + q2) / 2 * (t2 - t1).total_seconds() / 60

        # duty ratio for solenoids controlling medical air and oxygen flows
        di_i, di_o = calculate_pid_duty_ratio(p3)
        control_solenoid(SI_PIN, di_i)
        control_solenoid(SO_PIN, di_o)

        ti = (t2 - start_time).total_seconds()
        send_to_display(t2, p3, q2, vi)

        logger.debug("Ptarget: %.1f, Pcurrent: %.1f, Duty_Ratio: %.2f" % (Variables.pip_target, p3, di_i))

    # Store tidal volume for expiratory phase net volume calculation
    INSP_TOTAL_VOLUME = vi

    # Send pip to GUI
    mqtt.sender(mqtt.PIP_TOPIC, round(pip, 1))
    logger.info("[%.4f] Pip is : %.3f " % (ti, pip))

    logger.info("Leaving inspiratory phase.")


def exp_phase():
    """ expiratory phase tasks """
    logger.info("Entering expiratory phase...")

    global INSP_TOTAL_VOLUME, TIME_REF_MINUTE_VOL, MINUTE_VOLUME
    start_time = datetime.now()
    t1, t2 = start_time, start_time
    ti = 0
    q1, q2 = 0, 0
    vi, v_tot = 0, 0

    control_solenoid(SI_PIN, DUTY_RATIO_0)
    control_solenoid(SO_PIN, DUTY_RATIO_0)
    control_solenoid(SE_PIN, DUTY_RATIO_100)

    # Start calculating minute volume
    if TIME_REF_MINUTE_VOL is None:
        TIME_REF_MINUTE_VOL = start_time

    while ti < T_EX:

        send_pressure_data()

        t1 = t2
        q1 = q2
        q2, p3 = get_average_flow_rate_and_pressure(EXP_FLOW)
        t2 = datetime.now()

        # Calculate volume
        vi = 1000 * (q1 + q2) / 2 * (t2 - t1).total_seconds() / 60
        v_tot += vi
        ti = (t2 - start_time).total_seconds()

        # Handle minute volume calculations
        if (t2 - TIME_REF_MINUTE_VOL).total_seconds() < 60:
            logger.debug("<<< EXP >> vi=%.1f min_vol=%.1f", (vi, MINUTE_VOLUME))
            MINUTE_VOLUME += vi
        else:
            logger.debug("<<< EXP - RESET >> vi=%.1f min_vol=%.1f", (vi, MINUTE_VOLUME))
            submit_minute_vol(t2)

        send_to_display(t2, p3, (-1 * q2), (INSP_TOTAL_VOLUME - v_tot))
        logger.debug("ti = %.4f,     vi = %.1f" % (ti, vi))

    logger.info("<< CHART >> Actual tidal volume delivered : %.3f mL " % v_tot)
    mqtt.sender(mqtt.ACTUAL_TIDAL_VOLUME_TOPIC, round(v_tot))
    INSP_TOTAL_VOLUME = 0
    logger.info("Leaving expiratory phase.")


def send_pressure_data():
    """ send the pressure parameters to display unit via mqtt """

    global last_p1, last_p2, last_p3, last_p4

    p1, p2, p3, p4 = Variables.p1, Variables.p2, Variables.p3, Variables.p4

    payload = {
        'delta_p1': p1 - last_p1,
        'delta_p2': p2 - last_p2,
        'delta_p3': p3 - last_p3,
        'delta_p4': p4 - last_p4
    }
    mqtt.sender(mqtt.PRESSURE_DATA_TOPIC, payload)

    last_p1 = p1
    last_p2 = p2
    last_p3 = p3
    last_p4 = p4

    logger.debug(payload)


def submit_minute_vol(reset_time):
    global TIME_REF_MINUTE_VOL, MINUTE_VOLUME

    # Send minute volume to GUI
    mqtt.sender(mqtt.MINUTE_VOLUME_TOPIC, round(MINUTE_VOLUME))
    logger.debug("<<< SUBMIT >> min_vol=%.1f", MINUTE_VOLUME)

    # Reset minute volume calculation
    TIME_REF_MINUTE_VOL = reset_time
    MINUTE_VOLUME = 0


def wait_phase():
    """ waiting phase tasks """
    logger.info("Entering wait phase...")
    control_solenoid(SI_PIN, DUTY_RATIO_0)
    control_solenoid(SO_PIN, DUTY_RATIO_0)
    control_solenoid(SE_PIN, DUTY_RATIO_0)
    time.sleep(T_WT)
    logger.info("Leaving wait phase.")


def calc_respiratory_params():
    """ calculate inspiratory time and expiratory time using parameters set via UI """
    global T_IN, T_EX
    one_breath_time = 60 / Variables.rr
    T_IN = one_breath_time * 1 / (1 + Variables.ie)
    T_EX = one_breath_time * Variables.ie / (1 + Variables.ie)


def calc_pressure_offsests():
    """ Sensor readings for atmospheric pressure results in more than 0 cmH20.
        This offset is calculated and stored so that the future readings can be compensated. """
    time.sleep(2)

    p1_offset, p2_offset, p3_offset, p4_offset = 0, 0, 0, 0
    no_samples = 5

    for i in range(no_samples):
        p1_offset += Variables.p1
        p2_offset += Variables.p2
        p3_offset += Variables.p3
        p4_offset += Variables.p4
        time.sleep(1)

    Variables.p1_offset = p1_offset / no_samples
    Variables.p2_offset = p2_offset / no_samples
    Variables.p3_offset = p3_offset / no_samples
    Variables.p4_offset = p4_offset / no_samples

    logger.debug("Pressure offsets : p1 = %.1f, p2 = %.1f, p3 = %.1f, p4 = %.1f "
                 % (Variables.p1_offset, Variables.p2_offset, Variables.p3_offset, Variables.p4_offset))


def init_parameters():
    """ Initialize the parameters """
    global PWM_I, PWM_O, sensing_service, mqtt, pid, alarms

    # Initialize PWM pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(SI_PIN, GPIO.OUT)
    GPIO.setup(SO_PIN, GPIO.OUT)
    GPIO.setup(SE_PIN, GPIO.OUT)

    PWM_I = GPIO.PWM(SI_PIN, PWM_FREQ)
    PWM_O = GPIO.PWM(SO_PIN, PWM_FREQ)

    # Start the MQTT transceiver to communicate with GUI
    mqtt = MQTTTransceiver()

    # Initialize AlarmManager
    alarms = AlarmManager(mqtt)

    # Initially solenoids are all open
    PWM_I.start(DUTY_RATIO_100)
    PWM_O.start(DUTY_RATIO_100)
    control_solenoid(SE_PIN, DUTY_RATIO_100)

    # Start the sensor reading service
    sensing_service = SensorReaderService()

    # Calculate any pressure offsets
    calc_pressure_offsests()

    # Initialize PID Controller
    pid = PID(Variables.Kp, Variables.Ki, Variables.Kd)
    pid.SetPoint = Variables.pip_target
    pid.setSampleTime(Variables.pid_sampling_period)

    calc_respiratory_params()


def update_user_settings():
    """ User can change certain settings via GUI. Utilize the latest user settings for calculations """

    # update the target pressure in pid controller
    pid.SetPoint = Variables.pip_target

    # use the latest input parameters set via UI
    calc_respiratory_params()


def close_all_solenoids(delay):
    # Set the solenoids to OFF state
    control_solenoid(SI_PIN, DUTY_RATIO_0)
    control_solenoid(SO_PIN, DUTY_RATIO_0)
    control_solenoid(SE_PIN, DUTY_RATIO_0)
    time.sleep(delay)


#######################################################################################################

try:
    init_parameters()

    # Calibration should start after a trigger from user with a valid flow rate
    while Variables.calib_flow_rate < 0:
        time.sleep(2)

    # Calibrate the flow meter
    Ki, Ke = calibrate_flow_meter(Variables.calib_flow_rate)

    while True:
        insp_phase()
        exp_phase()
        # wait_phase()

        # Update user settings set via GUI for next cycle
        update_user_settings()

finally:
    mqtt.clean_up()  # clean up mqtt service
    close_all_solenoids(2)  # Set all solenoids to desired states before exiting
    print("\nExiting. Good bye...\n")
