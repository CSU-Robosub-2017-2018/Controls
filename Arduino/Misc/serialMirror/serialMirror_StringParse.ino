#include<Servo.h>

const int INPUT_SIZE = 29;

int i = 0;
int j = 0;
char input[INPUT_SIZE + 1];
unsigned int speedArray[6];

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  if (Serial.available() > 0) {
    byte inputSize = Serial.readBytes(input, INPUT_SIZE);
    Serial.println(input); 
    input[inputSize] = 0;
    
    char *tmp;
    int i = 0;
    tmp = strtok(input, ",");
    while(tmp) {
      speedArray[i++] = atoi(tmp);
      tmp = strtok(NULL, ",");
    }
    
    for (int j = 0; j < 6; j++) {
      Serial.println(speedArray[j]);
    }
    
    j = j + 1; 
    Serial.print("--- \nSerial: ");
    Serial.print(j);
    Serial.println("\n---");
  }
}
    
