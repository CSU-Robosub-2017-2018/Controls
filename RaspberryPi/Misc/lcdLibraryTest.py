import lcddriver
from time import *

lcd = lcddriver.lcd()

lcd.lcd_display_string("Hello world!", 1)
sleep(1.5)
lcd.lcd_clear()
lcd.lcd_display_string("My name is", 1)
lcd.lcd_display_string("picorder", 2)
sleep(1.5)
lcd.lcd_clear()
lcd.lcd_display_string("I am a Raspberry", 1)
lcd.lcd_display_string("Pi", 2)
sleep(1.5)
lcd.lcd_clear()
