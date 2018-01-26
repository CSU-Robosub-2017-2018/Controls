#!/usr/bin/env python

import lcddriver
from mpu6050 import mpu6050
import math

sensor = mpu6050(0x69)
lcd = lcddriver.lcd()

while True:
    accel_data = sensor.get_accel_data()
    pitch = math.atan2(accel_data['z'],accel_data['y'])
    roll = math.atan2(accel_data['z'],accel_data['x'])

    print(pitch)
    print(roll)

    lcd.lcd_display_string("pitch: " + str(round(math.degrees(pitch),2)), 1)
    lcd.lcd_display_string("roll: " + str(round(math.degrees(roll),2)), 2)
