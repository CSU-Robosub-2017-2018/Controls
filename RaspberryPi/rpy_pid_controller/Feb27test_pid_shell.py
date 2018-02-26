from RaspberryPi.rpy_pid_controller.pid.pid_controller_bno055 import pid_controller
from RaspberryPi.rpy_pid_controller.devices.BNO055 import BNO055
import time

class pid_wrapper:

    def __init__(self, imu):
        if imu.begin() is not True:
            print("Error initializing device")
            exit()
        time.sleep(1)

        self.pid_pitch = pid_controller(imu, 0, BNO055.VECTOR_EULER)
        self.pid_roll = pid_controller(imu, 1, BNO055.VECTOR_EULER)
        self.pid_yaw = pid_controller(imu, 2, BNO055.VECTOR_EULER)

    def get_pid(self):
        return {self.pid_pitch.get_pid(), self.pid_roll.get_pid(), self.pid_yaw.get_pid()}

    def set_targets(self, targets):
        self.pid_pitch.set_target_angle(targets[0])
        self.pid_roll.set_target_angle(targets[1])
        self.pid_yaw.set_target_angle(targets[2])

    def run(self):
        self.pid_pitch.run()
        self.pid_roll.run()
        self.pid_yaw.run()
