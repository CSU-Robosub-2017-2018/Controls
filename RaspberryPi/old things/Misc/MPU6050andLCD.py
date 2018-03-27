#!/usr/bin/env python

import lcddriver
from mpu6050 import mpu6050
import math

sensor = mpu6050(0x69)
lcd = lcddriver.lcd()

while True:
    accel_data = sensor.get_accel_data()
    string = "x: "
    string = string + str(round(accel_data['x'],2))
    string = string + " y: "
    string = string + str(round(accel_data['y'],2))
    string2 = "z: "
    string2 = string2 + str(round(accel_data['z'],2))
    print(string + " " + string2)
    lcd.lcd_display_string(string, 1)
    lcd.lcd_display_string(string2, 2)
