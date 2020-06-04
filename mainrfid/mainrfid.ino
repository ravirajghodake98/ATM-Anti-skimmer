#include<SoftwareSerial.h>
SoftwareSerial myser(8,9);
#define M1 13
#define M2 3

String A = "3E0067A226DD";
String B = "3E0067A78876";
String x;
char y;
void setup() 
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  myser.begin(9600);
  pinMode(M1,OUTPUT);
  digitalWrite(M1,LOW);
  pinMode(M2,OUTPUT);
  digitalWrite(M2,LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0)
  {
    y = Serial.read();
     if(y == 's' )
    {
        while(!(myser.available()>0))
        {
        }
        x = myser.readString();
         
      if(x == A )
      {
        Serial.println("f1");
      }
      if(x == B )
      {
        Serial.println("f2");
      }
    }
    while(!(Serial.available()>0))
        {
        }
        y = Serial.read();
        if(y == 'y')
        {
          digitalWrite(M1,HIGH);
          digitalWrite(M2,LOW);
        }
        else
        {
          digitalWrite(M1,LOW);
          digitalWrite(M2,LOW);
        }
  }
}
