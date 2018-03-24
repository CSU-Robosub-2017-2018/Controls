from Speed import test
from time import sleep

sp = test()
sp.setActive(0)
sp.writeActive()
sleep(1)

try:
    while True:
        user_in = input("Enter Axis: ")
        sp.setActive(user_in)
        sp.writeActive()
        print("Written!")
    
except:
    print("End of Test")
