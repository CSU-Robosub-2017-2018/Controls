from devices.BNO055 import BNO055
from pid.pid_controller_bno055 import pid_controller
import time

imu = BNO055()
if imu.begin() is not True:
    print("Error initializing device")
    exit()
time.sleep(1)

pid_pitch = pid_controller(imu, 1, BNO055.VECTOR_EULER)
pid_roll = pid_controller(imu, 2, BNO055.VECTOR_EULER)
pid_yaw = pid_controller(imu, 3, BNO055.VECTOR_EULER)
pid_pitch.run()
pid_roll.run()
pid_yaw.run()

"""Main"""
while True:
    print("pitch: " + str(pid_pitch.get_pid()))
    print("roll: " + str(pid_roll.get_pid()))
    print("yaw: " + str(pid_yaw.get_pid()))
    time.sleep(.5)