#include <Servo.h>
//Servo
Servo esc1;
Servo esc2;
Servo esc3;
Servo esc4;
Servo esc5;
Servo esc6;

//Error Pin
int ErrorPin = 22;

//PWM output pin assignments
const int PWM_out_pin1 = 1;
const int PWM_out_pin2 = 2;
const int PWM_out_pin3 = 3;
const int PWM_out_pin4 = 4;
const int PWM_out_pin5 = 5;
const int PWM_out_pin6 = 6;

// motor switch pin assignments(HIGH/LOW)
const int motor1 = 23;
const int motor2 = 25;
const int motor3 = 27;
const int motor4 = 29;
const int motor5 = 31;
const int motor6 = 33;

//States (Arm, Disarm, Error)
const int Arm = 1;
const int Disarm = 0;
const int ErrorClear = 2;
int CurrentState = 0;
int State;

//Char Array of state and PWM values
int i = 0;
int j = 0;
const int INPUT_SIZE = 29;
char input[INPUT_SIZE + 1];
unsigned int speedArray[6];

//Timeout variables
int currentTime = 0;
const int TIME_OUT = 1000;

//PWM Levels of each motor pair
int PWM_out_level1;
int PWM_out_level2;
int PWM_out_level3;
int PWM_out_level4;
int PWM_out_level5;
int PWM_out_level6;

void setup() {
  //initialize serial communications
  Serial.begin(19200);

  //Setting pins to outputs
  pinMode(ErrorPin, OUTPUT);
  pinMode(motor1, OUTPUT);
  pinMode(motor2, OUTPUT);
  pinMode(motor3, OUTPUT);
  pinMode(motor4, OUTPUT);
  pinMode(motor5, OUTPUT);
  pinMode(motor6, OUTPUT);

  closerelays();
}

void detachmotors() {
  esc1.detach();
  esc2.detach();
  esc3.detach();
  esc4.detach();
  esc5.detach();
  esc6.detach();
  Serial.println("PWM pins have been detached");
}

void attachmotors() {
  esc1.attach(PWM_out_pin1);
  esc2.attach(PWM_out_pin2);
  esc3.attach(PWM_out_pin3);
  esc4.attach(PWM_out_pin4);
  esc5.attach(PWM_out_pin5);
  esc6.attach(PWM_out_pin6);
  Serial.println("PWM pins have been attached");
}

void closerelays() {
  digitalWrite(motor1, HIGH);
  digitalWrite(motor2, HIGH);
  digitalWrite(motor3, HIGH);
  digitalWrite(motor4, HIGH);
  digitalWrite(motor5, HIGH);
  digitalWrite(motor6, HIGH);
  Serial.println("Relays have been closed");
}

void openrelays() {
  digitalWrite(motor1, LOW);
  digitalWrite(motor2, LOW);
  digitalWrite(motor3, LOW);
  digitalWrite(motor4, LOW);
  digitalWrite(motor5, LOW);
  digitalWrite(motor6, LOW);
  Serial.println("Relays have been opened");
}

void WritePWMs() {
  //Assigns PWM value to desired port
  esc1.writeMicroseconds(PWM_out_level1);
  esc2.writeMicroseconds(PWM_out_level2);
  esc3.writeMicroseconds(PWM_out_level3);
  esc4.writeMicroseconds(PWM_out_level4);
  esc5.writeMicroseconds(PWM_out_level5);
  esc6.writeMicroseconds(PWM_out_level6);

  //Sends information back to the sender
  for (int j = 0; j < 6; j++) {
    Serial.print("PWM ");
    Serial.print(j);
    Serial.print(" assigned to: ");
    Serial.println(speedArray[j]);
  }//for(int j = 0...
}

void readSerial() {
  byte inputSize = Serial.readBytes(input, INPUT_SIZE);
  Serial.println(input);
  input[inputSize] = 0;

  char *tmp;
  int i = 0;
  tmp = strtok(input, ",");
  while (tmp) {
    speedArray[i++] = atoi(tmp);
    tmp = strtok(NULL, ",");
  }
}

void error() {
  Serial.println("Error Detected");
  digitalWrite(ErrorPin, HIGH);
  openrelays();
  detachmotors();
  CurrentState = 2;
}

//Main Code
void loop() {
  if (Serial.available() > 0) { //use this around where I am looking for serial information
    currentTime = 0;
    readSerial();
    State = speedArray[0];

    //Checks for the next value read in to be
    if (State >= 1000 && CurrentState == Arm) {
      PWM_out_level1 = State;
      PWM_out_level2 = speedArray[1];
      PWM_out_level3 = speedArray[2];
      PWM_out_level4 = speedArray[3];
      PWM_out_level5 = speedArray[4];
      PWM_out_level6 = speedArray[5];

      WritePWMs();
    }//if state>=1000

    //Checks for first int read in to equal 1
    else if (State == Arm) {
      //Update current state to arm
      CurrentState = Arm;
      attachmotors();
    } //end of if state == Arm

    //Disarm motors by detaching pins
    else if (State == Disarm) { //Disarm and detatch servo
      CurrentState = Disarm;
      closerelays();
      detachmotors();
    } // end of if Disarm

    //After error has taken place, does an error clear and returns to disarm
    else if (State == ErrorClear && CurrentState == ErrorClear) { //Error
      digitalWrite(ErrorPin, LOW);
      closerelays();
      CurrentState = Disarm;
    }//end of if ErrorClear

    else {
      Serial.println("Bad Serial Communication");
    }
  }//if Serial.available

  //CurrentCheck (Halleffects)
  //Temperature Check (Themisters)

  if (currentTime < TIME_OUT + 1 && CurrentState == Arm) {
    currentTime++;
    Serial.println(currentTime);
  }
  if (currentTime > TIME_OUT && CurrentState != 2) {
    error();
    Serial.println("System timed out!");
  }

  //Want to periodically check hall effects while this code runs.

}//Void Loop

