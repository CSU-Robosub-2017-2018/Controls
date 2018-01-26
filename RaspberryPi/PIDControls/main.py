import time
import PID


while True:
    PID.update()
    time.sleep(1)
