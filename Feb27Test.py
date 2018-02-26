from RaspberryPi.rpy_pid_controller.Feb27test_pid_shell import pid_wrapper
from RaspberryPi.rpy_arduino_motorcontroller.MotorController_string import MotorController
from RaspberryPi.rpy_pid_controller.devices.BNO055 import BNO055
from RaspberryPi.helpers import helpers
from serial import Serial


imu = BNO055()
pid = pid_wrapper(imu)

serial = Serial(helpers.find_arduino()[0])
motors = MotorController(serial)

targets = {180, 180, imu.getVector(BNO055.VECTOR_EULER)[3]} #FIXME Need Correct target angles and correct orientation yaw angle.
pid.set_targets(targets)
pid.run()

armed = False
while not armed:
