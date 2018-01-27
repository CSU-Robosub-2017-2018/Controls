"""
Author: Nick Baron 1/27/2018
Description: This program is a test PID. I have been struggling to understand
 how this pid's output will scale with the PWM signal that i need to generate.

 To be run on a raspberry pi with a MPU6050: https://www.invensense.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf
 Made from this diagram: https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Pid-feedback-nct-int-correct.png/640px-Pid-feedback-nct-int-correct.png
"""
import time
import math
from mpu6050 import mpu6050

#PID constants
Kp = 3.0
Ki = 0.001
Kd = 2

#drivers
mpu = mpu6050(0x69)

# User Constants
target_angle = 90 #degrees

#setup constants
error_sum = 0
error_prev = 0

try:
    while True:
        mpu_data = mpu.get_accel_data(True)
        current_angle = math.degrees(math.atan2(1,1))
        error = target_angle - current_angle

        pid_p = Kp*error

        error_sum = error_sum + error
        pid_i = Ki*error_sum

        pid_d = Kd*(error_prev - error)
        error_prev = error

        pid = pid_p + pid_i + pid_d

        print("error: " + str(error))
        print("pid" + str(pid))
finally:
    print("closing stuff")
