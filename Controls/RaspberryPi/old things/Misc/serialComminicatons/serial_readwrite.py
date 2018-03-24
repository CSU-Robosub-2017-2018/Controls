import serial
import time

ser = serial.Serial("/dev/ttyACM0", 9600)

default = int(1000)

print("Setting default to %s" %default)
ser.write(str(default).encode())
while True:
    time.sleep(2)
    read_serial = ser.read(8)
    print("Current: %s" %read_serial)
    print("Waiting for input.")
    user_in = int(input())
    ser.write(str(user_in).encode())

    
