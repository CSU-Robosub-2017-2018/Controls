import sys
sys.path.append("/home/nick/Github/Controls/RaspberryPi/")
sys.path.append("/home/nick/Github/DataLogger")
from RaspberryPi.rpy_pid_controller.Feb27test_pid_shell import pid_wrapper
from RaspberryPi.rpy_motorcontroller.MotorController_hat import MotorController
from RaspberryPi.rpy_pid_controller.devices.mpu6050 import mpu6050
from time import sleep


imu = mpu6050(0x68)
pid = pid_wrapper(imu)

motors = MotorController()

targets = [0, 0] #FIXME Need Correct target angles and correct orientation yaw angle.
pid.set_targets(targets)
pid.run()

try:
    while True:
        while not motors.armed:
            print(str(imu.get_accel_data()))
            if imu.get_accel_data()['z'] < -8: #FIXME add ability to be within range.
                motors.arm()
                print("armed")
                sleep(5)
            sleep(0.25)

        while motors.armed:
            print(str(imu.get_accel_data()))
            if imu.get_accel_data()['z'] < -8:
                motors.disarm()
                print("disarmed")
                sleep(5)
            else:
                pidNum = pid.get_pid()
                for i in range(0, len(pidNum)):
                    if pidNum[i] > motors.pwm_max-motors.pwm_norm:
                        pidNum[i] = motors.pwm_max-motors.pwm_norm
                    elif pidNum[i] < motors.pwm_min-motors.pwm_norm:
                        pidNum[i] = motors.pwm_min-motors.pwm_norm
                    motors.write(i, motors.pwm_norm+pidNum[i], motors.pwm_norm-pidNum[i])
            sleep(0.25)

finally:
    pid.stop()
    motors.disarm()
