# Author Nick Baron
# Date 1/25/2018
# Description: This program is meant as an example of a PID controller.
# This will read the angle of an MPU6050 and attempt to correct the angle back to gravity.

import time as clock
from mpu6050 import mpu6050
import math


class PID:

    def __init__(self):
        print("welcome to pid")
        self.mpu = mpu6050(0x69)
        self.Kp = 3.55
        self.Ki = 0.005
        self.Kd = 2.05
        self.prevTime = 0
        self.time = clock.time()
        self.desiredAngle = 0 #FIXME find the desired angle
        self.pid_i = 0
        self.prevError = 0
        self.throttle = 1500  #this is the deadband for the throttle. >1500 is forward >1500 is backward

    def update(self):
        print("update")
        prevTime = self.time
        self.time = clock.time()
        elapsedTime = (self.time - prevTime) / 1000

        angles = self.mpu.get_accel_data()
        currentAngle = math.atan2(angles['x'], angles['z'])

        print("angle: " + str(currentAngle))

        error = currentAngle - self.desiredAngle
        print(error)
        pid_p = self.Kp * error

        if -0.2 < error < 0.2:
            self.pid_i = self.pid_i + (self.Ki * error)

        pid_d = self.Kd * ((error - self.prevError)/elapsedTime)

        pid = pid_p + self.pid_i + pid_d

        print("pid: " + str(pid))

        self.prevError = error
