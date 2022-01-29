#include <Servo.h>
Servo lock;
void setup() {
Serial.begin(9600);
pinMode(12,OUTPUT);
lock.attach(9);
lock.write(0);
while(!Serial){}
}

void loop() {
  while(Serial.available())
  {
    blnk();
    Serial.read();
  }
}

void blnk()
{
  digitalWrite(12,HIGH);
  for(int i=1;i<=90;i++)
  {
    delay(10);
    lock.write(i);
  }
  delay(3000);
  digitalWrite(12,LOW);
  for(int i=90;i>=1;i--)
  {
    delay(10);
    lock.write(i);
  }
}
