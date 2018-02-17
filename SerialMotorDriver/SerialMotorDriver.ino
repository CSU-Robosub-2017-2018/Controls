#include <Servo.h>

Servo servos[6];
unsigned int new_info[6];
const int normal_pwm[] = {1500, 1500, 1500, 1500, 1500, 1500};
int max_pwm = 2000;
int min_pwm = 1000;

const int INPUT_SIZE = 29;
char input[INPUT_SIZE + 1];

bool armed = false;

const int time_out = 1000;
int current_time = 0;

void arm() {
  if (armed) {
    Serial.print("Cannot arm and already armed thing!");
  }
  else {
    for (int i = 0; i < 6; i++) {
      servos[i].attach(i + 2);
    }
    armed = true;
    write_pwm(normal_pwm);
    Serial.println("armed");
  }
}

void disarm() {
  if (!armed) {
    Serial.println("Cannot disarm an already disarmed thing!");
  }
  else {
    for (int i = 0; i < 6; i++) {
      servos[i].detach();
    }
    armed = false;
    Serial.println("disarmed");
  }
}

void write_pwm(int speeds[6]) {
  if (!armed) {
    Serial.print("Cannot write when not armed");
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
  Serial.println("write");
}

void read_serial() {
  byte inputSize = Serial.readBytes(input, INPUT_SIZE);
  Serial.println(input);
  input[inputSize] = 0;

  char *tmp;
  int i = 0;
  tmp = strtok(input, ",");
  while (tmp) {
    new_info[i++] = atoi(tmp);
    tmp = strtok(NULL, ",");
  }
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
  arm();
}

void loop() {
  if (Serial.available() > 0) {
    current_time = 0;
    read_serial();
    if (new_info[0] > 10 && armed) {
      write_pwm(new_info);
    }
    else if (new_info[0] == 1 && !armed) {
      arm();
    }
    else if (new_info[0] == 0 && armed) {
      disarm();
    }
    else {
      Serial.print("bad serial comm");
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
