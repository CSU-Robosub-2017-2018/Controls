import time
import PID

pid = PID()

while True:
    pid.update()
    time.sleep(1)
