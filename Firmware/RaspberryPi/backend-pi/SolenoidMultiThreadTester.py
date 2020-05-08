from datetime import datetime
from PWMController import PWMController
import time

SOL_I = 10
SOL_E = 20
PWM_PERIOD = 0.5
threads_map = {}


def control_solenoid(pin, duty_ratio):
    # read four pressure sensors from the smbus and return actual values
    print("Entering control_solenoid()...")
    on_time = PWM_PERIOD * duty_ratio
    off_time = PWM_PERIOD * (1 - duty_ratio)

    if pin in threads_map:
        threads_map[pin].stop()
        threads_map[pin].join()
        print("Main: Stopped existing thread")

    t = PWMController(datetime.now().strftime('%Y%m%d%H%M%S%f'), pin, on_time, off_time)
    threads_map[pin] = t

    # Don't want these threads to run when the main program is terminated
    t.daemon = True
    t.start()
    print("Main: Started thread")

    time.sleep(3)

    print("Leaving control_solenoid().")


######################################################################3


while True:
    control_solenoid(SOL_I, 0.2)
    control_solenoid(SOL_E, 0.8)
