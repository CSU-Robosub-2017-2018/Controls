"""
Author: Nick Baron (830278807)
Date: 2/15/2018
Description: This class writes info over USB to an arduino to control pwm for ESC manipulation. There are two states: Armed and Disarmed.
"""

import time
import threading

class MotorController:

    armed = False

    def __init__(self, serialDevice):
        self.serialDevice = serialDevice
        self.data = {6, 1500, 1500, 1500, 1500, 1500, 1500}

    def arm(self):
        if not self.armed:
            self.data = {5, 1500, 1500, 1500, 1500, 1500, 1500}
            self.serialDevice.write()
            self.armed = True
            self.thread = threading.Thread(target=self.update, args=())
            self.thread.daemon = True  # Daemonize thread
            self.thread.start()  # Start the execution

    def disarm(self):
        if self.armed:
            self.data = {6, 1500, 1500, 1500, 1500, 1500, 1500}
            self.serialDevice.write()
            self.armed = False

    def update(self):
        while self.armed:
            self.write()
            time.sleep(.25)

    def set_speed(self, axis, speed0, speed1):
        if self.armed:
            self.data[2 * axis + 1] = speed0
            self.data[2 * axis + 2] = speed1

    def write(self):
        try:
            s = str(self.data[0])
            for i in range(1, len(self.data)):
                s += "," + str(self.data)
            self.serialDevice.write(s)
            if not self.serialDevice.read() == s:
                print("[ERROR] values may not have written properly!")
        except:
            print("[ERROR] serial write failed!")

