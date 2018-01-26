import time
import PID

PID()

while True:
    PID.update()
    time.sleep(1)
