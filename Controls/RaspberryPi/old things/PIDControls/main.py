import time
from PID import PID

pid = PID()

while True:
    pid.update()
    time.sleep(.2)
