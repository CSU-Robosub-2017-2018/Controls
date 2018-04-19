"""
Author: Nick Baron
Date: 3/22/2018
Description: This is a test class for a game controller using the inputs librbry. It gets and prints the max and min values of the controller that is being used.
"""

from inputs import get_gamepad

x = [0,0]
y = [0,0]
z = [0, 0]
rx = [0, 0]
ry = [0, 0]
rz = [0, 0]


try:
    while True:
        try:
            events = get_gamepad()
            for event in events:
                if event.code == "ABS_X":
                    x[0] = max(event.state, x[0])
                    x[1] = min(event.state, x[1])
                elif event.code == "ABS_Y":
                    y[0] = max(event.state, y[0])
                    y[1] = min(event.state, y[1])
                elif event.code == "ABS_Z":
                    z[0] = max(event.state, z[0])
                    z[1] = min(event.state, z[1])

                elif event.code == "ABS_RY":
                    ry[0] = max(event.state, ry[0])
                    ry[1] = min(event.state, ry[1])
                elif event.code == "ABS_RX":
                    rx[0] = max(event.state, rx[0])
                    rx[1] = min(event.state, rx[1])
                elif event.code == "ABS_RZ":
                    rz = max(event.state, rz)
                elif event.code == "SYN_REPORT":
                    nothing = 0
                else:
                    print(event.code, event.state)
                print(x,y,z,rx,ry,rz)
        except:
            print('disarm')
finally:
    print("large disarm")