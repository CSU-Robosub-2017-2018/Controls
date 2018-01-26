# Author Nick Baron
# Date 1/25/2018
# Description: This program is meant as an example of a PID controller.
# This will read the angle of an MPU6050 and attempt to correct the angle back to gravity.

import time as clock
import mpu6050 as mpu
import math


class PID:

    def __init__(self, Kp = 3.55, Ki = 0.005, Kd = 2.05):
        print("welcome to pid")
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
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

        angles = mpu.get_accel_data()
        currentAngle = math.atan2(angles[0], angles[1])

        print("angle: " + currentAngle)

        error = currentAngle - self.desiredAngle
        pid_p = self.Kp * error

        if error in range(-3, 3):
            self.pid_i = self.pid_i + (self.Ki * error)

        pid_d = self.Kd * ((error - self.prevError)/elapsedTime)

        pid = pid_p + self.pid_i + pid_d

        print("pid: " + pid)




