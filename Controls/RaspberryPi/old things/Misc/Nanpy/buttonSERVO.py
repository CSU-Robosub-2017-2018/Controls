from nanpy import (ArduinoApi, SerialManager, Servo)
from time import sleep

#This program is know to crash on first run. If it fails
#on the first run, rerun it. If the button is held down,
#the arduino is known to crash casuing the program to exit.

servoIncriment = 45
sleepTime = .5

servoPin = 3
buttonPin = 8
buttonState = 0
servoRun = servoIncriment

try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")
    

#Setup arduino pins like in arduino IDE

servo = Servo(servoPin)
a.pinMode(buttonPin, a.INPUT)
servo.write(0)

try:
    while True:
        buttonState = a.digitalRead(buttonPin)
        print(" Button State: {}" .format(buttonState))
        if buttonState:
            if servoRun > 180:
                servoRun = 0
            servo.write(servoRun)
            print("Servo Runs to: {}" .format(servoRun))
            servoRun += servoIncriment
            sleep(sleepTime)
        buttonState = False
            
except:
    servoRun = 0
    print("Servo EXITING")
    servo.write(0)

    
