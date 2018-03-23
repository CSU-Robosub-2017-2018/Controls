"""
Author: Nick Baron (830278807)
Date: 2/15/2018
Description: This class writes info over USB to an arduino to control pwm for ESC manipulation. There are two states: Armed and Disarmed.
"""

import time
import threading
import serial
from RaspberryPi.helpers import helpers

class MotorController:

    armed = False
    pwm_norm = 1500
    pwm_max = 2000
    pwm_min = 1000

    def __init__(self, serialDevice, Debug = False):
        self.Debug = Debug
        self.serialDevice = serialDevice
        self.data = {6, 1500, 1500, 1500, 1500, 1500, 1500}

    def arm(self):
        if not self.armed:
            if self.Debug:
                print("Armed")
            self.data = {5, 1500, 1500, 1500, 1500, 1500, 1500}
            self.serialDevice.write()
            self.armed = True
            self.thread = threading.Thread(target=self.update, args=())
            self.thread.daemon = True  # Daemonize thread
            self.thread.start()  # Start the execution

    def disarm(self):
        if self.armed:
            if self.Debug:
                print("Disrmed")
            self.data = {6, 1500, 1500, 1500, 1500, 1500, 1500}
            self.serialDevice.write()
            self.armed = False

    def update(self):
        while self.armed:
            if self.Debug:
                print("Update")
                print(str(self.data))
            self.write()
            time.sleep(.25)

    def set_speed(self, axis, speed0, speed1):
        if self.armed:
            self.data[2 * axis + 1] = speed0
            self.data[2 * axis + 2] = speed1
            if self.Debug:
                print("Set_Speed")
                print(str(axis) + " " + str(speed0) + " " + str(speed1))

    def write(self):
        try:
            if self.Debug:
                print("Write")
            s = str(self.data[0])
            for i in range(1, len(self.data)):
                s += "," + str(self.data)
            self.serialDevice.write(s)
            if not self.serialDevice.read() == s:
                print("[ERROR] values may not have written properly!")
        except:
            print("[ERROR] serial write failed!")

    def clear(self):
        for i in range(0,3):
            self.set_speed(i, self.pwm_norm, self.pwm_norm)


serial = serial.Serial(helpers.find_arduino())
motors = MotorController(serial, Debug=True)
print("Motors Started")
motors.arm()
print("Motors Armed")

try:
    while True:
        motors.set_speed(0, 1400, 1600)
        motors.set_speed(1, 1600, 1400)
        motors.set_speed(2, 1400, 1600)
        time.sleep(2)
        motors.clear()
        time.sleep(2)
finally:
    motors.disarm()
    serial.close()


