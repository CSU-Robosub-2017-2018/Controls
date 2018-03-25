import sys
#sys.path.append("/home/pi/Github/Adafruit_Python_PCA9685")
import Adafruit_PCA9685
from time import sleep

class MotorController:

    armed = False
    frequency = 50

    dead_bit = 320
    max_bit = 425
    min_bit = 213

    dead_us = 1500
    max_us = 2000
    min_us = 1000

    def __init__(self, ):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self.frequency)
        self.pulse_per_bit = self.get_ppb(self.frequency)

    def get_ppb(self, freq):
        self.pwm.set_pwm_freq(freq)
        pulse_length = 1000000.0  # 1,000,000 us per second
        pulse_length = pulse_length / freq
        print(str(pulse_length) + "us per period")
        pulse_length = pulse_length / 4096  # 12 bits of resolution
        print(str(pulse_length) + "us per bit")
        return pulse_length

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def get_bit(self, microsecond):
        #320 = 1500us
        #425 = 2000us
        #213 = 1000us
        if microsecond >= self.max_us:
            bit = self.max_bit
        elif microsecond <= self.min_us:
            bit = self.min_bit
        elif microsecond > self.dead_us+50 and microsecond < self.max_us:
            bit = self.map(microsecond, self.dead_us, self.max_us, self.dead_bit, self.max_bit)
        elif microsecond > self.min_us and microsecond < self.dead_us-50:
            bit = self.map(microsecond, self.min_us, self.dead_us, self.min_bit, self.dead_bit)
        elif microsecond == 0:
            bit = 0
        else:
            bit = 320
        #bit = int(round(microsecond / self.pulse_per_bit))
        print("us: " + str(microsecond) + " => bit:" + str(bit))
        return int(round(bit))

    def set_microseconds(self, channel, microsecond):
        self.pwm.set_pwm(channel, 0, self.get_bit(microsecond))

    def set_all_microseconds(self, microsecond):
        for i in range(0, 6):
            self.pwm.set_pwm(i, 0, self.get_bit(microsecond))

    def arm(self):
        print("Arm")
        self.set_all_microseconds(1500)
        self.armed = True

    def disarm(self):
        print("Disarm")
        self.set_all_microseconds(0)
        self.armed = False

    def write(self, axis, ms0, ms1):
        print("Write")
        if self.armed:
            self.set_microseconds(2 * axis, ms0)
            self.set_microseconds(2 * axis + 1, ms1)