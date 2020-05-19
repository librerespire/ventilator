from PID import PID
import time
import os.path

targetT = 10
P = 10
I = 1
D = 1
sampling_time = 0.5

pid = PID(P, I, D)
pid.SetPoint = targetT
pid.setSampleTime(sampling_time)

count = 0
pressureArray = [0, 1, 4, 7, 9, 7, 6, 5, 7, 8, 10, 10]


def readPressure():
    return pressureArray[count]


while count < 12:
    # read pressure data
    pressure = readPressure()

    pid.update(pressure)
    targetPwm = pid.output
    targetPwm = max(min(int(targetPwm), 100), 0)

    print("Target: %.1f | Current: %.1f | PWM: %s %%" % (targetT, pressure, targetPwm))

    # Set PWM expansion channel 0 to the target setting
    # pwmExp.setupDriver(0, targetPwm, 0)

    time.sleep(sampling_time-0.005)
    count += 1
