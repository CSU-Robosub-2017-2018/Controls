
from RaspberryPi.rpy_pid_controller.pid.pid_controller_6050 import pid_controller

class pid_wrapper:

    def __init__(self, mpu):
        self.pid_pitch = pid_controller(mpu, 'x', 'z')
        self.pid_roll = pid_controller(mpu, 'y', 'z')
        self.headers = ["Pitch_PID", "Roll_PID"]
        self.data = []
        self.running = False

    def get_headers(self):
        return self.headers

    def get_data(self):
        return [str(self.pid_pitch.get_pid()), str(self.pid_roll.get_pid())]

    def get_pid(self):
        return [self.pid_pitch.get_pid(), self.pid_roll.get_pid()]

    def get_speeds(self):
        pidNum = self.get_pid()
        return [pidNum[0], -pidNum[0], pidNum[1], pidNum[1], 0, 0]


    def set_targets(self, targets):
        self.pid_pitch.set_target_angle(targets[0])
        self.pid_roll.set_target_angle(targets[1])

    def set_pid(self,p,i,d):
        self.pid_pitch.set_Kp(p)
        self.pid_pitch.set_Ki(i)
        self.pid_pitch.set_Kd(d)
        self.pid_roll.set_Kp(p)
        self.pid_roll.set_Ki(i)
        self.pid_roll.set_Kd(d)

    def run(self):
        self.running = True

        self.pid_pitch.run()
        self.pid_roll.run()

    def stop(self):
        self.running = False

        self.pid_pitch.stop()
        self.pid_roll.stop()
