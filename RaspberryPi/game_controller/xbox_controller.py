
from inputs import get_gamepad
from RaspberryPi.helpers.helpers import map
import threading

class XboxController:

    def __init__(self):
        self.headers = ["XB0","XB1","XB2","XB3","XB4","XB5"]
        self.data = [0, 0, 0, 0, 0, 0]
        self.writing = ["", "", ""]
        self.norm = 0
        self.start_btn = False
        self.select_btn = False
        self.armed = False
        self.running = False
        self.joystick_dead = 3000
        self.trigger_dead = 40
        self.pid = [3, 0.001, 2]

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
                        self.handle_joystick(event.code, 2, event.state)
                    elif event.code == "ABS_X":
                        self.handle_joystick(event.code, 1, -event.state)
                    elif event.code == "BTN_THUMBL":
                        nothing = 0

                    # Right Stick
                    elif event.code == "ABS_RY":
                        self.handle_joystick(event.code, 0, -event.state)
                    elif event.code == "ABS_RX":
                        self.handle_joystick(event.code, 1, -event.state)

                    elif event.code == "BTN_THUMBR":
                        nothing = 0

                    # Triggers
                    elif event.code == "ABS_Z":
                        self.handle_trigger(event.code, 0, event.state)
                    elif event.code == "ABS_RZ":
                        self.handle_trigger(event.code, 0, event.state)

                    # Bumpers
                    elif event.code == "BTN_TL":
                        if event.state == 1 and self.writing[1] == "":
                            self.writing[1] = event.code

                            self.data[2] = self.norm - 200

                        elif event.state == 0 and self.writing[1] == event.code:
                            self.data[2] = self.norm
                            self.data[3] = self.norm
                            self.writing[1] = ""
                    elif event.code == "BTN_TR":
                        if event.state == 1 and self.writing[1] == "":
                            self.writing[1] = event.code

                            self.data[2] = self.norm + 200
                            self.data[3] = self.norm - 200

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


    def get_pid(self):
        return self.pid

    def reset_speeds(self):
        self.data = [0, 0, 0, 0, 0, 0]
        self.writing = ["", "", ""]


    def set_armed(self):
        if self.start_btn and self.select_btn:
            if self.armed:
                print("Controller disarmed")
                self.armed = False
            else:
                print("Controller Armed")
                self.armed = True


    def handle_joystick(self, code, axis, state):
        if abs(state) > self.joystick_dead and self.writing[axis] == "":
            self.writing[axis] = code
        elif abs(state) < self.joystick_dead and self.writing[axis] == code:
            self.writing[axis] = ""
        if self.writing[axis] == code:
            if abs(state) > self.joystick_dead:
                value = map(state, -32768, 32767, 500, -500)
                self.data[2 * axis] = self.norm + value
                if 'ABS_X' == code or "ABS_RY" == code:
                    value = -value
                self.data[2 * axis + 1] = self.norm + value
            else:
                self.data[2 * axis] = self.norm
                self.data[2 * axis + 1] = self.norm

    def handle_trigger(self, code, axis, state):
        if abs(state) > self.trigger_dead and self.writing[0] == "":
            self.writing[axis] = code
        elif abs(state) < self.trigger_dead and self.writing[0] == code:
            self.writing[axis] = ""
        if self.writing[axis] == code:
            if abs(state) > self.trigger_dead:
                value = map(state, 0, 255, 0, -300)
                if 'R' in code:
                    value = -value
                self.data[2 * axis] = self.norm + value
                self.data[2 * axis + 1] = self.norm + value
            else:
                self.data[2 * axis] = self.norm
                self.data[2 * axis + 1] = self.norm


