#define TAG_LEN 11
char target_tag[] = {0x03, 0x0E, 0x00, 0x00, 0x06, 0x07, 0x0A, 0x07, 0x08, 0x08, 0x07, 0x06 };
//rfid1 = {'3','E','0','0','6','7','A','7','8','8','7','6'}
int count = 0;
byte bytes_read=0;
   char tag_read[TAG_LEN];
  // code to request tag data goes here
void setup()
{
  Serial.begin(9600);
}
void loop()
{
  if(Serial.available()>0)
  {
   for(int i=0;i<12;i++)
  {
    tag_read[i]=Serial.read();
  }
  Serial.println(tag_read);
  for(int i=0;i<12;i++)
  {
    if(tag_read[i]== target_tag[i])
    {
      count++;
    }
  }
  Serial.println ("count ");
  Serial.println(count);
  if (count == 12)
  {
    Serial.println("matched");
  }
  }#include <SoftwareSerial.h> //Helps in Pin management
#include <string.h> //Helps in String Manipulation
#define EM_18_TX_PIN 9 //Pin to Read from Em-18 Reader
#define EM_18_RX_PIN 10 //Dummy Declaration
int GateOpenPin = 13;
SoftwareSerial serialEM18DREADER(EM_18_TX_PIN, EM_18_RX_PIN); //Defines Software Serial to EM-18 Reader.
// Now connect EM-18 Pin to D-09 Pin on Arduino.
// With such use, you need not unpin to write to Arduino.
//Variables to manage Reading RFID Data
int count = 0;
char RFIDtag[12] = {0}; //RFID Card number is Stored here after being read from EM-18 Reader
boolean newData = false;
//AuthTags is the list of Authorised RFID Card Numbers that you read from Serial Monitor.
//I have put only two here. If you want to add more numbers, then put , after the {"10004B6BD9E6"} and press enter.
// Then Put your new Numbers like this {"#####..."}, and then press enter and repeat the process
char AuthTags[][12] = {
  {"10004B50E7EC"},
  {"10004B6BD9E6"}
};

void setup()  {
  Serial.begin(9600);
  while (!Serial) {
    ;//Waits for Aruduino to get ready
  }
  Serial.println("Arduino Ready");

  serialEM18DREADER.begin(9600);
  while (!serialEM18DREADER) {
    ;//Waits for EM-18 Reader to get ready
  }
  Serial.println("EM-18 Ready");
  while (Serial.available() > 0 ) {
    Serial.read();
  }
}

void loop() {
  if (serialEM18DREADER.available() > 0)
  {
    count = 0;
    while (count < 12)
    {
      while (!serialEM18DREADER.available()) {
      }
      RFIDtag[count++] = serialEM18DREADER.read();
    }
    if (RFIDtag)// If RFIDtag vairable has data then process else continue
    {
      if (memcmp(RFIDtag, AuthTags, 12) == 0)
      { Serial.println(RFIDtag);//Displays the RFIDTag if found in the authorised list.
        //You may use following funtion to generate a High Pulse on Pin No 13 to trigger the Gate Opening

        digitalWrite(GateOpenPin, HIGH);
        delay(5000);//Wait for Five seconds to keep the gate open
        digitalWrite(GateOpenPin, LOW);//Lock the gate after Five second
        memset(RFIDtag, NULL, 12); //Fills the RFIDtag array with Null Chars. Something like flusing the variable empty.
      }
      else {
        Serial.println("RFID Not Found");
        memset(RFIDtag, NULL, 12);
      }
    }
  }
}
//  if (memcmp(tag_read, target_tag, TAG_LEN))
//  {
//    
//  Serial.println(tag_read);
//  Serial.println(target_tag);
//  Serial.println("matched");
//  }
      //do_something();
}
