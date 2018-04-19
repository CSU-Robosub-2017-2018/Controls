"""
Author: Nick Baron
Date: 2/1/2018
Description: This class is a PID contrller designed to be used with the MPU6050 class. It will run based on the accelerometer values that are converted into angles internally.
"""

import math
import time
import threading


class pid_controller:

    def __init__(self, mpu, axis1, axis2, target=0, update_rate=0.5):

        self.running = False

        # User Constants
        self.target_angle = target  # degrees
        self.update_rate = update_rate
        self.mpu = mpu #MPU6050 object passed in to constructor.
        self.axis1 = axis1
        self.axis2 = axis2

        # PID constants
        self.Kp = 2.6
        self.Ki = 0.001
        self.Kd = 2.5

        # setup constants
        self.error_sum = 0
        self.error_prev = 0
        self.loop_number = 0
        self.time_prev = time.time()
        self.pid_i = 0

        #Return Variables
        self.pid = 0

    def set_Kp(self, Kp):
        """
        Sets the proportional gain of the controller.
        :param Kp: The proportional gain.
        :return: Nothing
        """
        self.Kp = Kp

    def set_Ki(self, Ki):
        """
        Sets the integral gain of the pid controller.
        :param Ki: The integral gain.
        :return:
        """
        self.Ki = Ki

    def set_Kd(self, Kd):
        """
        Sets the derivative gain of the controller.
        :param Kd: The derivative gain.
        :return: Nothing.
        """
        self.Kd = Kd

    def get_Kp(self):
        """
        Returns the current proportional gain of the controller.
        :return: The current proportional gain.
        """
        return self.Kp

    def get_Ki(self):
        """
        Returns the current integral gain of the controller.
        :return: The current integral gain.
        """
        return self.Ki

    def get_Kd(self):
        """
        Returns the current derivative gain of the controller.
        :return: The current derivative gain.
        """
        return self.Kd

    def set_target_angle(self, target_angle=0):
        """
        This sets the target angle that the pid controller is trying to achieve.
        :param target_angle: Angle in degrees.
        :return: Nothing
        """
        self.target_angle = target_angle

    def calc_pid(self):
        while self.running:
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
        """
        This is the command that tells the pid to start running. This causes a new thread to be made which updates the pid in the background.
        :return: Nothing
        """
        self.running = True
        self.thread = threading.Thread(target=self.calc_pid, args=())
        self.thread.daemon = True  # Daemonize thread
        self.thread.start()  # Start the execution

    def stop(self):
        """
        This tells the PID thread to stop running.
        :return: Nothing
        """
        self.running = False

    def get_pid(self):
        """
        Gets the current pid value.
        :return: The PID value.
        """
        return self.pid



