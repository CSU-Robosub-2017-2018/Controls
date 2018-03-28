#include <Servo.h>

Servo servos[6];
const int servo_pins[] = {3, 5, 6, 9, 10, 11}; //Uno
//const int servo_pins[] = {2,3,4,5,6,7}; //Mega

bool armed = false;

void  for (int i = 0; i < 6; i++) {
    servos[i].attach(servo_pins[i]);
  }
  armed = true;
}
void disarm() {
  for (int i = 0; i < 6; i++) {
    servos[i].detach();
  }
  armed = false;
}




void setup()

void loop()
