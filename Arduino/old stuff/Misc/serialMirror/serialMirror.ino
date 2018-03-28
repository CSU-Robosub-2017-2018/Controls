
void setup()
{
  Serial.begin(250000);
  Serial.setTimeout(1);
}

void loop()
{
  if(Serial.available()){
    String val= Serial.readStringUntil('\n');
    Serial.println(val); 
  }
}

