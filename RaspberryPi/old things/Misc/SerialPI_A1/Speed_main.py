from Speed import test
from time import sleep

sp = test()
sp.setActive(0)
sp.setSpeed(1500,1500)
sleep(1)


for x in range(0, 2):
    for y in range(1000,2000,400):
        sp.setActive(x)
        sp.setSpeed(y,y)
        sleep(1)

print("End of Test")
