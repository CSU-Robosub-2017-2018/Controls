#Author: Nick Baron
#Date: 01/23/2018
#Description: This program is made to inteface with the arduino over a Serial USB connection. With this interface the Pi tells the arduino to put out certain PWM signals to control up to 6 ESC motors.
#When putting out 1500us the motors are standing still. Anything greater make the motors spin forward. Anything less makes the motors spin backwards.

try: #Is the code being run on a pi?
    import RPi.GPIO as GPIO
    import serial
    from threading import Timer
    from time import sleep
except: #is the code being run on a pc?
    import tests.serial as serial
    from tests.rpidevmocks import MockGPIO
    GPIO = MockGPIO()
    from threading import Timer
    from time import sleep

class ArduinoComm:

    debug = True
    speeds = [1500,1500,1500,1500,1500,1500] #Motor uSecond values: [x1,x2,y1,y2,z1,z2]

    dead = 1500
    Ulimit = 1750 #desired upper uS limit
    Llimit = 1250 #desired lower uS limit
    hardULimit = 2000
    hardLLimit = 1000

    updateRate = 0.2 #rate in seconds

    armed = False
    error = False

    gpioPin = 18 #FIXME get a good gpio pin

    def __init__(self):
        try:
            self.ser = serial.Serial("/dev/ttyACM0", 9600)
        except:
            print("ERROR: Cannot connect to serial port!")
            exit(1)
        try:
            GPIO.setmode(GPIO.BCM)
            # GPIO gpioPin set up as an input, pulled down, connected to 3V3 on error
            GPIO.setup(self.gpioPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            # when a rising edge is detected on port gpioPin, regardless of whatever
            # else is happening in the program, the function clearError will be run
            GPIO.add_event_detect(self.gpioPin,GPIO.RISING,callback=self.error,bouncetime=300)
        except:
            print("ERROR: Cannot setup GPIO Interrupt!")


    def initESC(self):
        #FIXME: write esc initialization
        self.debug = False
        
    def getArmed(self):
        return self.armed

    def write(self, newSpeeds):
        if len(newSpeeds) != len(self.speeds):
            print("WARNING: new speed arrays lengths don't match")
        elif self.armed:
            for e in range(0, len(self.speeds)):
                                if newSpeeds[e] > self.Ulimit:
                                        newSpeeds[e] = self.Ulimit
                                        if self.debug:
                                            print("WARNING: input exceeded upper limit")
                                if newSpeeds[e] < self.Llimit:
                                        newSpeeds[e] = self.Llimit
                                        if self.debug:
                                            print("WARNING: input exceeded lower limit")
            self.speeds = newSpeeds
            #returnVal = ",".join(str(e) for e in self.speeds)
            #self.ser.write(returnVal.encode())
            #print("write: " + returnVal)
        else:
            print("ERROR: cannot write while motors are not armed.")

    def update(self):
        if self.armed:
            returnVal = ",".join(str(e) for e in self.speeds)
            self.ser.write(returnVal.encode())
            if self.debug:
                print("update: " + returnVal)
            Timer(self.updateRate,self.update).start() #makes new thread that calls update every updateRate seconds
        else:
            print("WARNING: not armed, cannot update")

    def arm(self):
        self.ser.write("1".encode())
        if self.debug:
            print("armed")
        self.armed = True
        self.update()

    def disarm(self):
        self.ser.write("0".encode())
        if self.debug:
            print("disarmed")
            #self.ser.getCount() #testing off of arduino with custom serial class
        self.armed = False

    def getSpeed(self):
        return self.speeds

    def error(self, extra):
        #FIXME: handle errors
        if self.debug:
            print("error detected")
        self.write([1500,1500,1500,1500,1500,1500])
        self.armed = False
        self.error = True
        self.ser.write("3".encode())

    def getError(self):
        return self.error

    def clearError(self):
        self.error = False

    def cleanup(self):
        GPIO.cleanup()


