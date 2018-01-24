#include<Servo.h>

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  if(Serial.available()){
    String val= Serial.readString();
    Serial.println(val); 
  }
}

