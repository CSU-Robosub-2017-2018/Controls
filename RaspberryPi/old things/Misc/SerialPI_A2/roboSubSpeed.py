import serial
from time import sleep

class Speed:

    debug = False
    oneAxis = True
    state = 0
    speeds = [1500, 1500]

    def __init__(self):
        try:
            self.ser = serial.Serial("/dev/ttyACM0", 9600)
        except:
            print("ERROR: Cannot connect to serial port")
        self.disarm()

    def initESC(self, state = 0):
        for e in range(1,3):
            self.setState(e)
            self.setSpeed(1500,1500)
            sleep(1)
            self.setSpeed(2000,2000)
            sleep(1)
            self.setSpeed(1500,1500)

    def setState(self, state):
        if self.debug:
            print("Setting state: ", state)
        if state == 0:
            self.state = state
        elif (state > 0 and state < 4):
            if self.oneAxis:
                self.setSpeed(1500, 1500)
            self.state = state
        elif state == 4:
            print("DETECTED FEEDBACK ERROR!")
            self.disarm()
        else:
            print("ERROR: State not recognised: ", state)

    def getState(self):
        return self.state

    def setSpeed(self, speed0, speed1):
        self.speeds[0] = speed0
        self.speeds[1] = speed1
        returnVal = str(self.state) + "," + ",".join(str(e) for e in self.speeds)
        self.ser.write(returnVal.encode())
        print(returnVal)

    def getSpeed(self):
        return speeds

    def update(self, state, speed0, speed1):
        self.setState(state)
        self.setSpeed(speed0, speed1)

    def arm(self):
        for e in range(1,4):
            self.setState(e)
            self.setSpeed(1500,1500)

    def disarm(self):
        if self.state != 0:
            self.arm()
        self.update(0,1500,1500)

    

    
