"""
Author: Nick Baron 1/27/2018
Description: This program is a test PID. I have been struggling to understand
 how this pid's output will scale with the PWM signal that i need to generate.
 This program will write a CSV after iterating from -180 degrees to 180 degrees.

 Made from this diagram: https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Pid-feedback-nct-int-correct.png/640px-Pid-feedback-nct-int-correct.png
"""
import datetime
import os
import time

#PID constants
Kp = 1
Ki = 0.001
Kd = 1

#Drivers
dir_path = os.path.dirname(os.path.realpath(__file__))
now = datetime.datetime.now()
file = open(dir_path + "\P" + str(Kp) + "I" + str(Ki) + "D" + str(Kd) + now.strftime("-%Y-%m-%d-T%H-%M-%S") + ".csv", "w")

# User Constants
target_angle = 0 #degrees

#setup constants
error_sum = 0
error_prev = 0
time_prev = time.time()
pid_i = 0

time.sleep(.005)

file.write("CurrentError,CurrentPID\n")
for current_angle in range(-180, 181, 1):
    error = target_angle - current_angle

    pid_p = Kp * error
    print("p: " + str(pid_p))

    pid_i = pid_i + Ki * error
    print("i: " + str(pid_i))

    time_now = time.time()
    pid_d = Kd * ((error - error_prev)/(time_now - time_prev))
    print("d: " + str(pid_d))
    time_prev = time_now
    error_prev = error

    pid = pid_p + pid_i + pid_d

    error_str = "error: " + str(round(error, 2))
    pid_str = "pid: " + str(round(pid, 2))
    print(error_str)
    print(pid_str)
    file.write("" + str(round(error, 2)) + "," + str(round(pid, 2)) + "\n")
    time.sleep(.005)
file.close()

