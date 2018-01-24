from nanpy import (ArduinoApi, SerialManager, Servo)
from time import sleep

servoPin = 3

try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")
    

#Setup arduino pins like in arduino IDE

servo = Servo(servoPin)
servo.write(0)
userIn = 0;

try:
    while True:
       print("Current: ", userIn)
       userIn = input("Enter new: ")
       servo.write(userIn)
            
except:
    servoRun = 0
    print("Servo EXITING")
    servo.write(0)

    
