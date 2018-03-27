from nanpy import (ArduinoApi, SerialManager, Servo)
from time import sleep

try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")

servoPins = list()

for i in range(6):
    number = "";
    try:
        number = int(input("Enter ServoPWM pin number: "))
    except:
        print("End of user input!")
        break
    servoPins.append(number)


#Setup arduino pins like in arduino IDE

servos = []
for i in range(len(servoPins)):
    servos.append(Servo(servoPins[i]))
    servos[i].write(0)

try:
    while True:
        try:
            while True:
                for i in range(len(servos)):
                    print("Current State: ",i,": ", servos[i].read())
        except KeyboardInterrupt:
            serv = input("What servo? : ")
            change = input("What change? : ")
            servos[serv].write(change)
            print("Changed!")
            
except:
    servos = []
    for i in range(len(servos)):
        servos[i].detach()
    print("Servo EXITING")
