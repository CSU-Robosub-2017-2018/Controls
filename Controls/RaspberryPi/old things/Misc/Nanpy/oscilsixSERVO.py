from nanpy import (ArduinoApi, SerialManager, Servo)
from time import sleep

servoPins = [3,5,6,9,10,11]
angleInc = 45
currentChannel = 0
buttonPin = 13
buttonState = 0

numPins = len(servoPins)
currentServo = 0
currentAngle = 0
servo = []


try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")
    

#Setup arduino pins like in arduino IDE

a.pinMode(buttonPin, a.INPUT)
for m in servoPins:
        servo.append(Servo(m))

try:
    while True:
        buttonState = a.digitalRead(buttonPin)
        print(" Button State: {} Current Servo: {} Current Angle: {}" .format(buttonState, currentServo, currentAngle))
        if buttonState:
            servo[currentServo].write(0)
            currentAngle = 0
            currentServo += 1
            if currentServo > numPins:
                currentServo = 0
            sleep(1)
        buttonState = False
        servo[currentServo].write(currentAngle)
        currentAngle += angleInc
        if currentAngle > 180:
            currentAngle = 0
        sleep(1)
                    
except:
    print("Servo EXITING")
    for m in servo:
        m.detach()

    
