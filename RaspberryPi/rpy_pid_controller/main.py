from devices import mpu6050
from pid import pid_controller
import sys

"""Setup"""
mpu = mpu6050(0x69)
pid_pitch = pid_controller(mpu,'x', 'z')
pid_roll = pid_controller(mpu, 'y', 'z')
pid_yaw = pid_controller(mpu, 'x', 'y')

"""Main"""
while True:
    sys.stdout.write("")