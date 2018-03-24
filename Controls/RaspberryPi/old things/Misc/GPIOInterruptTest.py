import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
button = 18

def call_back(channel):
    print("Detect")

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button,GPIO.RISING,callback=call_back,bouncetime=300)

try:
    while True:
        print("Sleeping...")
        sleep(2)
except:
    GPIO.cleanup()
