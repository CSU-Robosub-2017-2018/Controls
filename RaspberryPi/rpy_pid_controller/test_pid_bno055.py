from RaspberryPi.rpy_pid_controller.devices.BNO055 import BNO055
from RaspberryPi.rpy_pid_controller.pid.pid_controller_bno055 import pid_controller
import time

imu = BNO055()
if imu.begin() is not True:
    print("Error initializing device")
    exit()
time.sleep(1)

pid_pitch = pid_controller(imu, 0, BNO055.VECTOR_EULER)
pid_roll = pid_controller(imu, 1, BNO055.VECTOR_EULER)
pid_yaw = pid_controller(imu, 2, BNO055.VECTOR_EULER)
pid_pitch.run()
pid_roll.run()
pid_yaw.run()

"""Main"""
while True:
    print("angles: " + str(imu.getVector(BNO055.VECTOR_EULER)))
    print("pitch: " + str(pid_pitch.get_pid()))
    print("roll: " + str(pid_roll.get_pid()))
    print("yaw: " + str(pid_yaw.get_pid()))
    time.sleep(.5)