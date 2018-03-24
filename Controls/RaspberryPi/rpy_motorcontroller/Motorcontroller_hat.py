import Adafruit_PCA9685 as pwm
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
        self.set_all_servo_pulse(1500)
        self.armed = True

    def disarm(self):
        self.set_all_servo_pulse(0)
        self.armed = False

    def write(self, axis, pulse0, pulse1):
        if self.armed:
            self.set_servo_pulse(2 * axis, pulse0)
            self.set_servo_pulse(2 * axis + 1, pulse1)

