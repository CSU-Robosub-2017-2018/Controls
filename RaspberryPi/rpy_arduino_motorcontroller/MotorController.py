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
        self.data = bytearray(14)

    def get_armed(self):
        return self.armed

    def arm(self):
        if not self.armed:
            self.data = int(5).to_bytes(14,'little')
            self.serialDevice.write()
            self.armed = True
            self.thread = threading.Thread(target=self.update, args=())
            self.thread.daemon = True  # Daemonize thread
            self.thread.start()  # Start the execution

    def disarm(self):
        if self.armed:
            self.data = int(6).to_bytes(14,'little')
            self.serialDevice.write()
            self.armed = False

    def update(self):
        while self.armed:
            self.data[0] = int(3).to_bytes(1,'big')
            self.write()
            time.sleep(.25)

    def set_speed(self, axis, speed0, speed1):
        if self.armed:
            speed0 = int(speed0).to_bytes(2,'big')
            speed1 = int(speed1).to_bytes(2,'big')
            


    def write(self):
        try:
            self.serialDevice.write(self.data)
            if not self.serialDevice.read() == input:
                print("[ERROR] values may not have written properly!")
        except:
            print("[ERROR] serial write failed!")

