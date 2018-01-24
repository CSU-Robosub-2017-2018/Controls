import serial
from time import sleep



class test:

    def __init__(self):
        try:
            self.ser = serial.Serial("/dev/ttyACM2", 9600)
        except:
            print("ERROR: Cannot connect to serial port")
        self.current = [0,1500,1500]

    def setSpeed(self, left, right):
        self.current[1] = left
        self.current[2] = right
        self.ser.write(''.join(str(e) for e in self.current).encode())
        

    def setActive(self, s):
        if s == 0:
            self.current[0] = 1
        elif s == 1:
            self.current[0] = 2
        elif s == 2:
            self.current[0] = 3
        else:
            print("Cannot set the active axis to: " , s)
            self.current[0] = s
        print(self.current[0])

    def writeActive(self):
        self.ser.write(str(self.current[0]).encode())
