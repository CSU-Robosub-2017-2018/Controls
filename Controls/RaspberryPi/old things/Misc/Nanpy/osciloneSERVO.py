from nanpy import (ArduinoApi, SerialManager, Servo)
from time import sleep

servoPin = 3
angleInc = 45


currentAngle = 0


try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")
    

#Setup arduino pins like in arduino IDE

a.pinMode(buttonPin, a.INPUT)
servo = Servo(m)

try:
    while True:
        buttonState = a.digitalRead(buttonPin)
        print("Current Angle: {}" .format(currentAngle))
        servo[currentServo].write(currentAngle)
        currentAngle += angleInc
        if currentAngle > 180:
            currentAngle = 0
        sleep(1)
                    
except:
    print("Servo EXITING")
    servo.detach()

    
