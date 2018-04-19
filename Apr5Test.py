"""
Author: Nick Baron
Date: 3/28/2018
Description: This is the main script that controls and initializes all systems for the sub during the apr 4th sub test.
"""

import sys
sys.path.append("/home/nick/github/Controls/RaspberryPi/")
sys.path.append("/home/nick/github/Datalogger/")
print(sys.path)
from RaspberryPi.rpy_pid_controller.Apr5test_pid_shell import pid_wrapper
from RaspberryPi.rpy_motorcontroller.MotorController_hat import MotorController
from RaspberryPi.rpy_pid_controller.devices.mpu6050 import mpu6050
from RaspberryPi.game_controller.xbox_controller import XboxController
from DataLogger import DataLogger
from writers.csv import csv
from time import sleep


writer = csv('APR4_')
logger = DataLogger(writer)

imu = mpu6050(0x68)
pid = pid_wrapper(imu)
motors = MotorController()
ctrlr = XboxController()

logger.add_device(imu)
logger.add_device(pid)
logger.add_device(motors)
logger.add_device(ctrlr)

targets = [0, 0] #FIXME Need Correct target angles and correct orientation yaw angle.
pid.set_targets(targets)
pid.run()
logger.start()
ctrlr.start()

ctrlrdata_old = ctrlrdata = ctrlr.get_speeds()
count = 0

try:
    while True:
        while not motors.armed:
            if ctrlr.armed:
                motors.arm()
                print("armed")
                sleep(1)

        while motors.armed:
            if not ctrlr.armed:
                motors.disarm()
                print("Disarmed")
                sleep(1)
            else:
                ctrlrdata = ctrlr.get_speeds()
                if ctrlrdata == ctrlrdata_old:
                    if count > 1000:
                        ctrlr.reset_speeds()
                    else:
                        count = count + 1
                else:
                    count = 0
                piddata = pid.get_speeds()

                print("Controller", str(ctrlrdata))
                print("PID", str(piddata))

                for i in range(0, 6):
                    speed = ctrlrdata[i] + piddata[i]
                    if speed > motors.pwm_max - motors.pwm_norm:
                        speed = motors.pwm_max - motors.pwm_norm
                    elif speed < motors.pwm_min - motors.pwm_norm:
                        speed = motors.pwm_min - motors.pwm_norm
                    motors.set_microseconds(i, motors.pwm_norm + speed)

                ctrlrdata_old = ctrlrdata

finally:
    logger.end()
    pid.stop()
    motors.disarm()



