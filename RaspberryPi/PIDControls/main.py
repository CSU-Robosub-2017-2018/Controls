import PID
import time

pid = PID()

while True:
    pid.update()
    time.sleep(1)