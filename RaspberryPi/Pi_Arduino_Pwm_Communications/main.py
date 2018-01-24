from time import sleep
from communications.ArduinoComm import ArduinoComm

a = ArduinoComm()

try:
    while True:
            s = (int)(input("Type 1: "))
            if s == 1:
                try:
                            a.arm()
                            sleep(5)
                            a.update()
                            while a.getArmed():
                                a.write([1500,3000,1200,1400,1900,2100])
                                sleep(1)
                                a.write([1300,2300,2600,800,0000,3000])
                                sleep(1)
                                
                except:
                    a.disarm()
except:
    a.cleanup()

