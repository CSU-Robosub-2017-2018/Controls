import RPi.GPIO as GPIO
from time import sleep

class Motor:

    def __init__(self, pin, frequency=50):
        self.frequency = frequency
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm=GPIO.PWM(pin, frequency)
        self.initializeESC()

    def initializeESC(self):
        self.pwm.start(self.convert(1000))  #starting pwm at min throttle
        sleep(1)
        self.pwm.ChangeDutyCycle(self.convert(2000)) #pwm at full throttle
        sleep(1)
        self.pwm.ChangeDutyCycle(self.convert(1100)) #pwm at slightly open throttle
        sleep(1)
        self.pwm.ChangeDutyCycle(self.convert(1000)) #close throttle

    def convert(self, time): #returns the ratio of a time given in us to the period of the frequency.
        return time/(1000000*(1/self.frequency))

    def write(self, time):
        self.pwm.ChangeDutyCycle(self.convert(time))
