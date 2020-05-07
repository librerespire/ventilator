# Controller v1.0
# 2020-05-08 1.05 AM (Melb)

#from DataManipulator import DataManipulator
import math
import time
from datetime import datetime
import threading
from SensorReader import SensorReader

NUMDER_OF_SENSORS = 4
pressure_data = [0] * 6

def threadSlice(pressure_data, index):
    sr = SensorReader(index)
    pressure = sr.read_pressure()
    pressure_data[index] = pressure

def read_data():
    # read four pressure sensors from the smbus and return actual values
    threads = list()
    for index in [1,3,4,5]:
        x = threading.Thread(target=threadSlice, args=(pressure_data, index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()

    return pressure_data[1], pressure_data[3], pressure_data[4], pressure_data[5]


# def calculate_k(p1, p2, flow_rate):
#     return flow_rate / math.sqrt(abs(p1 - p2))
#
#
# # With current settings flow meter will be calibrated over 5 seconds (nSamples * delay)
# def calibrate_flow_meter(flow_rate):
#     """ returns the calibrated k, calculated based on multiple pressure readings """
#     nSamples = 10  # average over 10 samples
#     delay = 0.5  # 0.5 seconds
#     n = 0
#     k = 0
#     # Take the average over 'nSamples' pressure readings, 'delay' seconds apart to calculate k
#     while n < nSamples:
#         p1, p2, p3, p4 = read_data()
#         k += calculate_k(p1, p2, flow_rate)
#         n += 1
#         time.sleep(delay)
#
#     k /= nSamples
#     print("Flow meter was calibrated. k = %.3f" % k)
#     return k
#
# def control_solenoid(pin, duty_ratio):
#     """ TODO: For now, digital out to the given pin with the given duty_ratio. Ideally this has to be in PWM. Till then,
#     e.g. duty_ratio=0.5 ON(100ms)-OFF(100ms)-ON(100ms)-OFF(100ms)... So need to be implemented on a separate thread
#     so that the calling function [e.g. insp_phase()] will not be on hold """
#     pass
#
#
# def get_average_volume_rate(is_insp_phase):
#     """ read p1 and p2 over 200 milliseconds and return average volume rate """
#
#     nSamples = 4  # average over 4 samples
#     delay = 0.05  # 50 milliseconds
#     n = 0
#     q = 0
#     # Take the average over 'nSamples' pressure readings, 'delay' seconds apart to calculate flow rate
#     while n < nSamples:
#         p1, p2, p3, p4 = read_data()
#         if (is_insp_phase):
#             q += k * math.sqrt(abs(p1 - p2))
#         else:
#             q += k * math.sqrt(abs(p3 - p4))
#
#         n += 1
#         time.sleep(delay)
#
#     return k / nSamples
#
#
# def calculate_pid_duty_ratio(demo_level):
#     """ TODO: implement the PID controller to determine the required duty ratio to achieve the desired pressure curve
#         Currently a temporary hack is implemented with demo_level """
#     duty_ratio = 0.8
#     if (demo_level == 1):
#         duty_ratio = 0.2
#
#     return duty_ratio
#
#
# def insp_phase(demo_level):
#     """ inspiratory phase tasks
#         demo_level is a temporary hack to introduce two flow rate levels until pid controller is implemented """
#
#     print("Entering inspiratory phase...")
#     start_time = datetime.now()
#     t1, t2 = start_time, start_time
#     ti = 0
#     q1, q2 = 0, 0
#     vi = 0
#
#     # Control solenoids
#     control_solenoid(PIN_S1, DUTY_RATIO_0)
#     control_solenoid(PIN_S2, DUTY_RATIO_0)
#
#     while ti < Ti and vi < Vt:
#         t1 = t2
#         q1 = q2
#         q2 = get_average_volume_rate(True)
#         t2 = datetime.now()
#
#         vi += (q1 + q2) / 2 * (t2 - t1).total_seconds() / 60
#
#         di = calculate_pid_duty_ratio(demo_level)
#         control_solenoid(PIN_S1, di)
#         control_solenoid(PIN_S2, DUTY_RATIO_0)
#
#         ti = (datetime.now() - start_time).total_seconds()
#         print(q2, vi, ti)
#
#     print("Leaving inspiratory phase.")
#
# def exp_phase():
#     """ expiratory phase tasks """
#     print("Entering expiratory phase...")
#     start_time = datetime.now()
#     t1, t2 = start_time, start_time
#     ti = 0
#     q1, q2 = 0, 0
#     vi = 0
#     p3 = Peep
#
#     control_solenoid(PIN_S1, DUTY_RATIO_0)
#     control_solenoid(PIN_S2, DUTY_RATIO_0)
#
#     while ti < Te and p3 <= Peep:
#         t1 = t2
#         q1 = q2
#         q2 = get_average_volume_rate(False)
#         t2 = datetime.now()
#
#         vi += (q1 + q2) / 2 * (t2 - t1).total_seconds() / 60
#
#         p1, p2, p3, p4 = read_data()
#         if p3 < Peep:
#             control_solenoid(PIN_S2, 0)
#
#         ti = (datetime.now() - start_time).total_seconds()
#         print(q2, vi, p3, ti)
#
#     print("Leaving expiratory phase.")
#     print("Actual tidal volume delivered : %.3f L " % vi)
#
#
# def wait_phase():
#     """ waiting phase tasks """
#     print("Entering wait phase...")
#     control_solenoid(PIN_S1, DUTY_RATIO_0)
#     control_solenoid(PIN_S2, DUTY_RATIO_0)
#     time.sleep(Tw)
#     print("Leaving wait phase.")
#
#
# #######################################################################################################
#
# # 12 here is the intended flow_rate for calibration in L/min
# k = calibrate_flow_meter(12)
#
# # print(k)
# # results = DataManipulator(1000, 964, 800, 700, k)
# # print("Flow rate : %.2f L/min " % results.get_flow_rate())
# # print("Inspiratory pressure : %.2f cmH2O " % results.get_insp_pressure() + "\n")
#
# # Constants
# PIN_S1 = 30     # PIN number for inspiratory solenoid
# PIN_S2 = 31     # PIN number for expiratory solenoid
# DUTY_RATIO_100 = 1
# DUTY_RATIO_0 = 0
#
# # Parameters
# Ti = 2     #  inspiratory time
# Te = 2     #  expiratory time
# Tw = 1     #  waiting time
# Vt = 2     #  tidal volume
# Pi = 2000  # peak inspiratory pressure in cmH2O
# Peep = 1200
#
# while True:
#     # slow flow rate
#     print("\n\nSlower flow rate cycle")
#     insp_phase(1)
#     exp_phase()
#     wait_phase()
#
#     # faster flow rate
#     print("\n\nFaster flow rate cycle")
#     insp_phase(2)
#     exp_phase()
#     wait_phase()

if __name__ == "__main__":
    print(read_data())
