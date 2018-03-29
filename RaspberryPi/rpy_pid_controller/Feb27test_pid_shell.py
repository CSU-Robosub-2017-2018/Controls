
from RaspberryPi.rpy_pid_controller.pid.pid_controller_6050 import pid_controller
import time

class pid_wrapper:

    def __init__(self, mpu):
        self.pid_pitch = pid_controller(mpu, 'x', 'z')
        self.pid_roll = pid_controller(mpu, 'y', 'z')
        self.headers = ["Pitch_PID", "Roll_PID"]
        self.data = []

    def get_headers(self):
        return self.headers

    def get_data(self):
        return [str(self.pid_pitch.get_pid()), str(self.pid_roll.get_pid())]

    def get_pid(self):
        return [self.pid_pitch.get_pid(), self.pid_roll.get_pid()]

    def set_targets(self, targets):
        self.pid_pitch.set_target_angle(targets[0])
        self.pid_roll.set_target_angle(targets[1])

    def run(self):
        self.pid_pitch.run()
        self.pid_roll.run()

    def stop(self):
        self.pid_pitch.stop()
        self.pid_roll.stop()
