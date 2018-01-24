from nanpy import (ArduinoApi, SerialManager)
from time import sleep;

ledPin =7
buttonPin = 8
ledState = False
buttonState = 0

try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")

#Setup arduino pins like in arduino IDE

a.pinMode(ledPin, a.OUTPUT)
a.pinMode(buttonPin, a.INPUT)

try:
    while True:
        buttonState = a.digitalRead(buttonPin)
        print(" Button State: {}" .format(buttonState))
        if buttonState:
            if ledState:
                a.digitalWrite(ledPin, a.LOW)
                ledState = False
                print("LED OFF")
                sleep(1)
            else:
                a.digitalWrite(ledPin, a.HIGH)
                ledState = True
                print("LED ON")
                sleep(1)
except:
    a.digitalWrite(ledPin, a.LOW)

    
