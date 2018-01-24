from time import sleep
from roboSubSpeed import Speed

sp = Speed()

print("--ARM--")
sp.arm()
print("--UPDATE--")
sp.update(1,2000,2000)
sp.update(2,2000,2000)
sp.update(3,2000,2000)
print("--DISARM--")
sp.disarm()
        
