#include <Servo.h>

Servo servos[6];
int servo_pins[] = {3,5,6,9,10,11} //Uno
//int servo_pins[] = {2,3,4,5,6,7} //Mega
unsigned int new_data[6];
const int normal_pwm[] = {1500, 1500, 1500, 1500, 1500, 1500};
int max_pwm = 2000;
int min_pwm = 1000;

bool armed = false;

const int time_out = 1000;
int current_time = 0;

void arm() {
  if (armed) {
    return;
  }
  else {
    for (int i = 0; i < 6; i++) {
      servos[i].attach(servo_pins[i]);
    }
    armed = true;
    write_pwm(normal_pwm);
  }
}

void disarm() {
  if (!armed) {
    return;
  }
  else {
    for (int i = 0; i < 6; i++) {
      servos[i].detach();
    }
    armed = false;
  }
}

void write_pwm(int speeds[6]) {
  if (!armed) {
    return;
  }
  for (int i = 0; i < 6; i++) {
    if (speeds[i] > max_pwm) {
      speeds[i] = max_pwm;
    }
    else if (speeds[i] < min_pwm) {
      speeds[i] = min_pwm;
    }
    servos[i].writeMicroseconds(speeds[i]);
  }
}

void read_serial() {
  byte new_bytes[];
  int data_length = Serial.readBytes(new_bytes,14);
   if (data_length > 0) {
    new_data[0] = new_bytes[0];
    for(int i = 1; i < sizeof(new_bytes); i = i + 2) {
      new_data[i] = normal_pwm[i] + (int(new_bytes[i])<<8) + int(new_bytes[i+1]);
    }
   }
   else {
    // ERROR
    delay(10)
   }
   memset(new_data, 0, sizeof(new_bytes));   // Clear contents of Buffer
   Serial.flush();
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
}

void loop() {
  if (Serial.available() > 0) {
    current_time = 0;
    read_serial();
    if (new_data[0] > 10 && armed) {
      write_pwm(new_data);
    }
    else if (new_data[0] == 5 && !armed) {
      arm();
    }
    else if (new_data[0] == 6 && armed) {
      disarm();
    }
    else {
      delay(1000);
    }
  }

  else if (current_time < time_out && armed) {
    current_time++;
    Serial.println(current_time);
  }
  else if (current_time >= time_out && armed) {
    disarm();
    delay(1000);
  }
  else {
    Serial.print(armed);
    Serial.print(" ");
    Serial.println(current_time);
  }
}
