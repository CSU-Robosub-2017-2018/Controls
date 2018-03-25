import sys
sys.path.append("/home/pi/Github/Adafruit_Python_PCA9685")
import Adafruit_PCA9685.PCA9685 as pwm
from time import sleep

class MotorController:

    def __init__(self):
        pwm.set_pwm_freq(50)
        self.armed = False

    def get_pulse(self, pulse):
        pulse_length = 1000000  # 1,000,000 us per second
        pulse_length //= 50  # 60 Hz
        print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096  # 12 bits of resolution
        print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        return pulse

    def set_servo_pulse(self, channel, pulse):
        pwm.set_pwm(channel, 0, self.get_pulse(pulse))

    def set_all_servo_pulse(self, pulse):
        pwm.set_all_pwm(0, self.get_pulse(pulse))

    def arm(self):
        print("Arm")
        self.set_all_servo_pulse(1500)
        self.armed = True

    def disarm(self):
        print("Disarm")
        self.set_all_servo_pulse(0)
        self.armed = False

    def write(self, axis, pulse0, pulse1):
        print("Write")
        if self.armed:
            self.set_servo_pulse(2 * axis, pulse0)
            self.set_servo_pulse(2 * axis + 1, pulse1)


motors = MotorController()
motors.arm()

try:
    while True:
        motors.write(1, 1500, 1600)
        motors.write(0, 2000, 1200)
        motors.write(2, 1000, 2000)
        sleep(2)
        motors.arm()
        sleep(2)

finally:
    motors.disarm()