from devices import mpu6050
from pid import pid_controller
import time

"""Setup"""
mpu = mpu6050(0x69)
pid_pitch = pid_controller(mpu,'x', 'z')
pid_roll = pid_controller(mpu, 'y', 'z')
pid_yaw = pid_controller(mpu, 'x', 'y')

"""Main"""
while True:
    print("pitch: " + str(pid_pitch.get_pid()))
    print("roll: " + str(pid_roll.get_pid()))
    print("yaw: " + str(pid_yaw.get_pid()))
    time.sleep(.5)