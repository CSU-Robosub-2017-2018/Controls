"""
Author: Nick Baron 2/1/2018
Description:
"""

import math
import time
import threading


class pid_controller:

    def __init__(self, mpu, axis1, axis2, target=0, update_rate=0.5):

        # User Constants
        self.target_angle = target  # degrees
        self.update_rate = update_rate
        self.mpu = mpu #MPU6050 object passed in to constructor.
        self.axis1 = axis1
        self.axis2 = axis2

        # PID constants
        self.Kp = 3.0
        self.Ki = 0.001
        self.Kd = 2

        # setup constants
        self.error_sum = 0
        self.error_prev = 0
        self.loop_number = 0
        self.time_prev = time.time()
        self.pid_i = 0

        #Return Variables
        self.pid = 0

    def set_Kp(self, Kp):
        self.Kp = Kp

    def set_Ki(self, Ki):
        self.Ki = Ki

    def set_Kd(self, Kd):
        self.Kd = Kd

    def get_Kp(self):
        return self.Kp

    def get_Ki(self):
        return self.Ki

    def get_Kd(self):
        return self.Kd

    def set_target_angle(self, target_angle=0):
        self.target_angle = target_angle

    def calc_pid(self):
        while True:
            mpu_data = self.mpu.get_accel_data(True)
            current_angle = math.degrees(math.atan2(mpu_data[self.axis1], mpu_data[self.axis2]))

            error = self.target_angle - current_angle

            pid_p = self.Kp * error
            #print("p: " + str(pid_p))

            self.pid_i = self.pid_i + self.Ki * error
            #print("i: " + str(self.pid_i))

            time_now = time.time()
            pid_d = self.Kd * ((error - self.error_prev) / (time_now - self.time_prev))
            #print("d: " + str(pid_d))
            self.time_prev = time_now
            self.error_prev = error

            self.pid = pid_p + self.pid_i + pid_d
            time.sleep(self.update_rate)

    def run(self):
        self.thread = threading.Thread(target=self.calc_pid, args=())
        self.thread.daemon = True  # Daemonize thread
        self.thread.start()  # Start the execution

    def stop(self):
        return "stop"

    def get_pid(self):
        return self.pid



