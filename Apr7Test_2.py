import sys
sys.path.append("/home/nick/github/Controls/RaspberryPi/")
sys.path.append("/home/nick/github/Datalogger/")
print(sys.path)
from RaspberryPi.rpy_pid_controller.Apr5test_pid_shell import pid_wrapper
from RaspberryPi.rpy_motorcontroller.MotorController_hat import MotorController
from RaspberryPi.rpy_pid_controller.devices.mpu6050 import mpu6050
from DataLogger import DataLogger
from writers.csv import csv
from time import sleep
import threading


writer = csv('APR7_2_')
logger = DataLogger(writer)

imu = mpu6050(0x68)
pid = pid_wrapper(imu)
motors = MotorController()

logger.add_device(imu)
logger.add_device(pid)
logger.add_device(motors)

targets = [0, 0] #FIXME Need Correct target angles and correct orientation yaw angle.
pid.set_targets(targets)
pid.set_pid(3, 0.001, 2)
pid.run()
logger.start()

def pid_help():
    while pid.running:
        pidNum = pid.get_pid()
        for i in range(0, len(pidNum)):
            if pidNum[i] > motors.pwm_max - motors.pwm_norm:
                pidNum[i] = motors.pwm_max - motors.pwm_norm
            elif pidNum[i] < motors.pwm_min - motors.pwm_norm:
                pidNum[i] = motors.pwm_min - motors.pwm_norm
            motors.write(i, motors.pwm_norm + pidNum[i], motors.pwm_norm - pidNum[i])
        sleep(0.25)

try:
    threading.Thread(target=pid_help).start()
    sleep(150)
    motors.arm()
    sleep(150)
    motors.write(2, 1600, 1600)
    sleep(5)
    motors.disarm()

finally:
    logger.end()
    pid.stop()
    motors.disarm()



