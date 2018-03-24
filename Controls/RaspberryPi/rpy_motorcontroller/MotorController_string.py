"""
Author: Nick Baron (830278807)
Date: 2/15/2018
Description: This class writes info over USB to an arduino to control pwm for ESC manipulation. There are two states: Armed and Disarmed.
"""

import time
import threading
import serial
import sys
sys.path.append("C:\\Users\\Nicholas Baron\\Documents\\GitHub\\Controls\\Controls\\RaspberryPi\\helpers")
import helpers

class MotorController:

    armed = False

    def __init__(self, arduino_serial):
        self.speeds = [6, 1500, 1500, 1500, 1500, 1500, 1500]
        self.serial = arduino_serial


    def arm(self):
        print("arm")
        self.speeds[0] = 5
        self.clear_speeds()
        self.armed = self.write()
        if self.armed:
            self.thread = threading.Thread(target=self.update, args=())
            self.thread.daemon = True  # Daemonize thread
            self.thread.start()  # Start the execution
            return True
        else:
            return False

    def disarm(self):
        print("disarm")
        self.speeds[0] = 6
        if self.write():
            self.armed = False
            return True
        else:
            return False

    def set_speeds(self, axis, speed0, speed1):
        print("set")
        self.speeds[2 * axis + 1] = speed0
        self.speeds[2 * axis + 2] = speed1

    def update(self):
        while self.write():
            time.sleep(.2)

    def write(self):
        s = (str(self.speeds).replace(" ", "")[1:-1] + "\n").encode()
        print("write " + str(s))
        self.serial.write(s)
        time.sleep(.5)
        sr = self.serial.read_until('\n')
        print(str(sr))
        if sr == s:
            return True
        else:
            return False

    def clear_speeds(self):
        for i in range(1, len(self.speeds)):
            self.speeds[i] = 1500


serial = serial.Serial(helpers.find_arduinos()[0], baudrate=250000, timeout=10)
motors = MotorController(serial)
motors.arm()

try:
    while motors.armed:
        motors.set_speeds(0, 1000, 2000)
        motors.set_speeds(0, 1100, 1900)
        motors.set_speeds(0, 1200, 1800)
        time.sleep(2)
        motors.clear_speeds()
        time.sleep(2)
finally:
    motors.disarm()
    serial.close()




