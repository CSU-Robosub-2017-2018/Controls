
from inputs import get_gamepad
from RaspberryPi.helpers.helpers import map
import threading

class XboxController:

    def __init__(self):
        self.headers = ["XB0","XB1","XB2","XB3","XB4","XB5"]
        self.data = [0,0,0,0,0,0]
        self.writing = ["", "", ""]
        self.norm = 0
        self.start_btn = False
        self.select_btn = False
        self.armed = False
        self.running = False
        self.joystick_dead = 3000
        self.trigger_dead = 40

    def get_headers(self):
        return self.headers

    def get_data(self):
        return [str(self.data[0]), str(self.data[1]), str(self.data[2]), str(self.data[3]),
                str(self.data[4]), str(self.data[5])]


    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True  # Daemonize thread
        self.thread.start()

    def stop(self):
        self.running = False

    def update(self):
        while self.running:
            try:
                events = get_gamepad()
                for event in events:

                    # Left Stick
                    if event.code == "ABS_Y":
                        if abs(event.state) > self.joystick_dead and self.writing[2] == "":
                            self.writing[2] = event.code
                        elif abs(event.state) < self.joystick_dead and self.writing[2] == event.code:
                            self.writing[2] = ""
                        if self.writing[2] == event.code:
                            if abs(event.state) > self.joystick_dead:
                                self.data[4] = self.norm + map(event.state, -32768, 32767, 500, -500)
                                self.data[5] = self.norm + map(event.state, -32768, 32767, 500, -500)
                            else:
                                self.data[4] = self.norm
                                self.data[5] = self.norm
                    elif event.code == "ABS_X":
                        if abs(event.state) > self.joystick_dead and self.writing[1] == "":
                            self.writing[1] = event.code
                        elif abs(event.state) < self.joystick_dead and self.writing[1] == event.code:
                            self.writing[1] = ""
                        if self.writing[1] == event.code:
                            if abs(event.state) > self.joystick_dead:
                                self.data[2] = self.norm + map(event.state, -32768, 32767, -500, 500)
                                self.data[3] = self.norm + map(event.state, -32768, 32767, -500, 500)
                            else:
                                self.data[2] = self.norm
                                self.data[3] = self.norm
                    elif event.code == "BTN_THUMBL":
                        nothing = 0

                    # Right Stick
                    elif event.code == "ABS_RY":
                        if abs(event.state) > self.joystick_dead and self.writing[0] == "":
                            self.writing[0] = event.code
                        elif abs(event.state) < self.joystick_dead and self.writing[0] == event.code:
                            self.writing[0] = ""
                        if self.writing[0] == event.code:
                            if abs(event.state) > self.joystick_dead:
                                self.data[0] = self.norm + map(event.state, -32768, 32767, -500, 500)
                                self.data[1] = self.norm - map(event.state, -32768, 32767, -500, 500)
                            else:
                                self.data[0] = self.norm
                                self.data[1] = self.norm
                    elif event.code == "ABS_RX":
                        if abs(event.state) > self.joystick_dead and self.writing[2] == "":
                            self.writing[2] = event.code
                        elif abs(event.state) < self.joystick_dead and self.writing[2] == event.code:
                            self.writing[2] = ""
                        if self.writing[2] == event.code:
                            if abs(event.state) > self.joystick_dead:
                                self.data[4] = self.norm + map(event.state, -32768, 32767, -500, 500)
                                self.data[5] = self.norm - map(event.state, -32768, 32767, -500, 500)
                            else:
                                self.data[4] = self.norm
                                self.data[5] = self.norm
                    elif event.code == "BTN_THUMBR":
                        nothing = 0

                    # Triggers
                    elif event.code == "ABS_Z":
                        if abs(event.state) > self.trigger_dead and self.writing[0] == "":
                            self.writing[0] = event.code
                        elif abs(event.state) < self.trigger_dead and self.writing[0] == event.code:
                            self.writing[0] = ""
                        if self.writing[0] == event.code:
                            if abs(event.state) > self.trigger_dead:
                                self.data[0] = self.norm + map(event.state, 0, 255, 0, -500)
                                self.data[1] = self.norm + map(event.state, 0, 255, 0, -500)
                            else:
                                self.data[0] = self.norm
                                self.data[1] = self.norm
                    elif event.code == "ABS_RZ":
                        if abs(event.state) > self.trigger_dead and self.writing[0] == "":
                            self.writing[0] = event.code
                        elif abs(event.state) < self.trigger_dead and self.writing[0] == event.code:
                            self.writing[0] = ""
                        if self.writing[0] == event.code:
                            if abs(event.state) > self.trigger_dead:
                                self.data[0] = self.norm + map(event.state, 0, 255, 0, 500)
                                self.data[1] = self.norm + map(event.state, 0, 255, 0, 500)
                            else:
                                self.data[0] = self.norm
                                self.data[1] = self.norm

                    # Bumpers
                    elif event.code == "BTN_TL":
                        if event.state == 1 and self.writing[1] == "":
                            self.writing[1] = event.code
                            self.data[2] = self.norm + 200
                            self.data[3] = self.norm - 200
                        elif event.state == 0 and self.writing[1] == event.code:
                            self.data[2] = self.norm
                            self.data[3] = self.norm
                            self.writing[1] = ""
                    elif event.code == "BTN_TR":
                        if event.state == 1 and self.writing[1] == "":
                            self.writing[1] = event.code
                            self.data[2] = self.norm - 200
                            self.data[3] = self.norm + 200
                        elif event.state == 0 and self.writing[1] == event.code:
                            self.writing[1] = ""
                            self.data[2] = self.norm
                            self.data[3] = self.norm

                    # Buttons
                    elif event.code == "BTN_NORTH":
                        nothing = 0
                    elif event.code == "BTN_SOUTH":
                        self.reset_speeds()
                    elif event.code == "BTN_EAST":
                        nothing = 0
                    elif event.code == "BTN_WEST":
                        nothing = 0

                    # D-Pad
                    elif event.code == "ABS_HAT0Y":
                        nothing = 0
                    elif event.code == "ABS_HAT0X":
                        nothing = 0

                    # Start-Select
                    elif event.code == "BTN_SELECT": #Start button on xbox one s controller
                        if event.state == 1:
                            self.start_btn = True
                        else:
                            self.start_btn = False
                        self.set_armed()
                    elif event.code == "BTN_START":
                        if event.state == 1:
                            self.select_btn = True
                        else:
                            self.select_btn = False
                        self.set_armed()

                    elif event.code == "SYN_REPORT":
                        nothing = 0
                    else:
                        self.data = [self.norm, self.norm, self.norm, self.norm, self.norm, self.norm]
            except:
                self.armed = False

    def get_speeds(self):
        return self.data

    def reset_speeds(self):
        self.data = [0, 0, 0, 0, 0, 0]

    def set_armed(self):
        if self.start_btn and self.select_btn:
            if self.armed:
                print("Controller disarmed")
                self.armed = False
            else:
                print("Controller Armed")
                self.armed = True

