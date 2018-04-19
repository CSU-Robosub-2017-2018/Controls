"""
Author: Nick Baron
Date: 3/28/2018
Desription: This is a pid wrapper that controlls all of the PID controllers that are being used for the april 4th sub test.
"""
from RaspberryPi.rpy_pid_controller.pid.pid_controller_6050 import pid_controller

class pid_wrapper:

    def __init__(self, mpu):
        """
        Initializes all of the pidcontrillers and the headres for the datalogger.
        :param mpu: The accelerometer that is being used for all of the PID controllers.
        """
        self.pid_pitch = pid_controller(mpu, 'x', 'z')
        self.pid_roll = pid_controller(mpu, 'y', 'z')
        self.headers = ["Pitch_PID", "Roll_PID"]
        self.data = []
        self.running = False

    def get_headers(self):
        """
        Retuns all of the header strings for the data logger.
        :return: Header string array.
        """
        return self.headers

    def get_data(self):
        """
        Returns all of the data information for the fdata logger.
        :return: Array of strings.
        """
        return [str(self.pid_pitch.get_pid()), str(self.pid_roll.get_pid())]

    def get_pid(self):
        """
        This gets the pid values for all of the pid controllers.
        :return: array of pid information.
        """
        return [self.pid_pitch.get_pid(), self.pid_roll.get_pid()]

    def get_speeds(self):
        """
        gets all of the pid information and returns that pid information as speed commands for motors.
        :return: Array of 6 ints representing motor speeds.
        """
        pidNum = self.get_pid()
        return [pidNum[0], -pidNum[0], pidNum[1], pidNum[1], 0, 0]


    def set_targets(self, targets):
        """
        Sets the targets of the pid controllers.
        :param targets: A degree.
        :return: Nothing
        """
        self.pid_pitch.set_target_angle(targets[0])
        self.pid_roll.set_target_angle(targets[1])

    def set_pid(self,p,i,d):
        """
        Sets the PID values for the pid controllers.
        :param p: Proportional
        :param i: Inegral
        :param d: Derivative
        :return: Nothing
        """
        self.pid_pitch.set_Kp(p)
        self.pid_pitch.set_Ki(i)
        self.pid_pitch.set_Kd(d)
        self.pid_roll.set_Kp(p)
        self.pid_roll.set_Ki(i)
        self.pid_roll.set_Kd(d)

    def run(self):
        """
        Tells the pid controller to start running.
        :return: Nothing
        """
        self.running = True

        self.pid_pitch.run()
        self.pid_roll.run()

    def stop(self):
        """
        Tells the PID controllers to stop.
        :return: Nothing.
        """
        self.running = False

        self.pid_pitch.stop()
        self.pid_roll.stop()
