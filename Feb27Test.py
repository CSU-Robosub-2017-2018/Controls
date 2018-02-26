from RaspberryPi.rpy_pid_controller.Feb27test_pid_shell import pid_wrapper
from RaspberryPi.rpy_arduino_motorcontroller.MotorController_string import MotorController
from RaspberryPi.rpy_pid_controller.devices.BNO055 import BNO055
from RaspberryPi.helpers import helpers
from serial import Serial
from time import sleep


imu = BNO055()
pid = pid_wrapper(imu)

serial = Serial(helpers.find_arduino()[0])
motors = MotorController(serial)

targets = {imu.getVector(BNO055.VECTOR_EULER)} #FIXME Need Correct target angles and correct orientation yaw angle.
pid.set_targets(targets)
pid.run()

try:
    while not motors.armed():
        if imu.getVector(BNO055.VECTOR_EULER)[0] == abs(360-targets[0]): #FIXME add ability to be within range.
            motors.arm()
            sleep(10)

    while motors.armed():
        if imu.getVector(BNO055.VECTOR_EULER)[0] == abs(360-targets[0]):
            motors.disarm()
        else:
            pidNum = pid.get_pid()
            for i in range(0, len(pidNum)):
                if pidNum[i] > motors.pwm_max-motors.pwm_norm:
                    pidNum[i] = motors.pwm_max-motors.pwm_norm
                elif pidNum[i] < motors.pwm_min-motors.pwm_norm:
                    pidNum[i] = motors.pwm_min-motors.pwm_norm
                motors.write(i,motors.pwm_norm+pidNum[i], motors.pwm_norm-pidNum[i])

finally:
    pid.stop()
    motors.disarm()
