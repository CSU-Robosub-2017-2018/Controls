import serial
import time

ser = serial.Serial("/dev/ttyACM1", 115200)

default = int(1000)

print("Setting default to %s" %default)
ser.write(str(default).encode())
read_serial = ser.readline()
print("Current: %s" %read_serial)
    
    
