"""
Author: Nick Baron 1/27/2018
Description: This program is a test PID. I have been struggling to understand
 how this pid's output will scale with the PWM signal that i need to generate.

 To be run on a raspberry pi with a MPU6050: https://www.invensense.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf
 Uses 2x16 lcd with i2c driver: https://www.amazon.com/gp/product/B01FDD3X98/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1
 Made from this diagram: https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Pid-feedback-nct-int-correct.png/640px-Pid-feedback-nct-int-correct.png
"""
import time
import math
from mpu6050 import mpu6050
import lcddriver

#PID constants
Kp = 3.0
Ki = 0.001
Kd = 2

#drivers
mpu = mpu6050(0x69)
lcd = lcddriver.lcd()

# User Constants
target_angle = 90 #degrees

#setup constants
error_sum = 0
error_prev = 0
loop_number = 0

try:
    while True:
        mpu_data = mpu.get_accel_data(True)
        current_angle = math.degrees(math.atan2(mpu_data['x'], mpu_data['z']))
        error = target_angle - current_angle

        pid_p = Kp*error

        error_sum = error_sum + error
        pid_i = Ki*error_sum

        pid_d = Kd*(error_prev - error)
        error_prev = error

        pid = pid_p + pid_i + pid_d

        lcd.lcd_display_string("error: " + str(round(error)),0)
        lcd.lcd_display_string("pid: " + str(round(pid)), 1)

        if loop_number > 1000:
            lcd.lcd_clear()
            time.sleep(.25)
            loop_number = 0
        else:
            time.sleep(.05)
            loop_number = loop_number + 1
finally:
    print("closing stuff")
    exit(0)
