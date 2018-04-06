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
            self.write()
            time.sleep(.25)

    def set_speed(self, axis, speed, speed1):
        if self.armed:
            speed = int(speed).to_bytes(2, 'big')
            speed += int(speed1).to_bytes(2, 'big')

            for i in range(0, len(speed)):
                self.data[2*axis+1+i] = speed[i]

    def write(self):
        try:
            self.serialDevice.write(self.data)
            if not self.serialDevice.read() == self.data:
                print("[ERROR] values may not have written properly!")
        except:
            print("[ERROR] serial write failed!")

