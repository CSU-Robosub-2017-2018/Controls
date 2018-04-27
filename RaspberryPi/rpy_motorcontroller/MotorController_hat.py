"""
Author: Nicholas Baron 830278807
Date: 3/25/2018
Description: This is a class that will allow the operator to communicate and write speeds to Robosub's ESCs axialy.
"""
import sys
sys.path.append("/home/nick/python_driver/Adafruit_Python_PCA9685")
sys.path.append("/home/nick/github/Controls/RaspberryPi/")
import Adafruit_PCA9685
from RaspberryPi.helpers.helpers import map

class MotorController:

    armed = False
    frequency = 50 #in hz

    dead_bit = 320
    max_bit = 425
    min_bit = 213

    pwm_norm = 1500
    pwm_max = 2000
    pwm_min = 1000

    act_num = 50 #the number of us off norm for the class to start writing information to the hat. Default 50 (same as dead band for esc)

    def __init__(self):
        """
        Initializes the motorcontroller setting the headers for the datalogger and starting the adafruit pwm hat.
        """
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self.frequency)
        self.pulse_per_bit = self.get_ppb(self.frequency)
        self.headers = ["x1", "x2", "y1", "y2", "z1", "z2"]
        self.data = [0, 0, 0, 0, 0, 0]

    def get_ppb(self, freq):
        """
        This allows the user to get the approximate bit value for a certain us value. It is not exact. The values can be tuned in a similar way to get_bit.
        :param freq: This is the frequency you would like to get the bit value for. Note: this will set the frequency for the pi hat in the process.
        :return: Returns and float that is the amount of us per bit of the adafruit hat.
        """
        self.pwm.set_pwm_freq(freq)
        pulse_length = 1000000.0  # 1,000,000 us per second
        pulse_length = pulse_length / freq
        print(str(pulse_length) + "us per period")
        pulse_length = pulse_length / 4096  # 12 bits of resolution
        print(str(pulse_length) + "us per bit")
        return pulse_length

    def get_bit(self, microsecond):
        """
        This is a finely tuned version of get_ppb. It will allow the user to get the exact bit value between 1000us and 2000us at 50Hz for the adafruit shield. USE THIS one.
        :param microsecond: This is the motorspeed that your want to get the bit value for.
        :return: The bit value corresponding to the input time.
        """
        #320 = 1500us
        #425 = 2000us
        #213 = 1000us
        if microsecond == 0:
            bit = 0
        elif microsecond >= self.pwm_max:
            bit = self.max_bit
        elif microsecond <= self.pwm_min:
            bit = self.min_bit
        elif microsecond > self.pwm_norm+self.act_num and microsecond < self.pwm_max:
            bit = map(microsecond, self.pwm_norm, self.pwm_max, self.dead_bit, self.max_bit)
        elif microsecond > self.pwm_min and microsecond < self.pwm_norm-self.act_num:
            bit = map(microsecond, self.pwm_min, self.pwm_norm, self.min_bit, self.dead_bit)
        else:
            bit = 320
        #bit = int(round(microsecond / self.pulse_per_bit))
        print("us: " + str(microsecond) + " => bit:" + str(bit))
        return int(round(bit))

    def set_batch_microseconds(self, us_array):
        """
        This will set all of the motors to the given values passed the the function.
        :param us_array: This is an array of 6 int that represent the motorspeeds. [x1, x2, y1, y2, z1, z2]
        :return: Nothing
        """
        self.data = us_array
        for i in range(0, 6):
            self.pwm.set_pwm(i, 0, us_array[i])

    def set_microseconds(self, channel, microsecond):
        """
        This will set the us of a specific channel to the given value.
        :param channel: The channel (0-6)
        :param microsecond: This is the time high that you want it set to.
        :return: Nothing
        """
        self.data[channel] = microsecond
        self.pwm.set_pwm(channel, 0, self.get_bit(microsecond))

    def set_all_microseconds(self, microsecond):
        """
        This function sets all 6 axial speeds to the same value.
        :param microsecond: the speed to set all motors to.
        :return: nothing
        """
        for i in range(0, 6):
            self.data[i] = microsecond
            self.pwm.set_pwm(i, 0, self.get_bit(microsecond))

    def get_headers(self):
        """
        Gets the headers for the datalogger.
        :return: An array of 6 strings representing the names of each bit of data for the datalogger.
        """
        return self.headers

    def get_data(self):
        """
        Gets the values of the motors for the data logger.
        :return: An array of 6 strings that are the data for each value of the datalogger.
        """
        return [str(self.data[0]), str(self.data[1]), str(self.data[2]), str(self.data[3]),
                str(self.data[4]), str(self.data[5])]

    def get_speeds(self):
        """
        Gets the values that the motors are currently set to.
        :return: An array of 6 ints representing the us values of the motors.
        """
        return self.data

    def arm(self):
        """
        This tells the motor controller to arm the motors. Sets the motors from 0us to 1500us.
        :return: Nothing.
        """
        print("Arm")
        self.set_all_microseconds(1500)
        self.armed = True

    def disarm(self):
        """
        This tells the motor controller to disarm the motors. Sets all motors to 0us time high.
        :return: Nothing
        """
        print("Disarm")
        self.set_all_microseconds(0)
        self.armed = False

    def write(self, axis, ms0, ms1):
        """
        This allows the user to write to the motor controller axialy. This is intended to be used for forward, up, and down movement.
        :param axis: The axis that you are writing to. [x, y, z]
        :param ms0: Motor-speed 0.
        :param ms1: Motor-speed 1.
        :return:
        """
        print("Write")
        if self.armed:
            self.set_microseconds(2 * axis, ms0)
            self.set_microseconds(2 * axis + 1, ms1)