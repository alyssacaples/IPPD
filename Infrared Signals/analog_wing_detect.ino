/*
  Analog input, analog output, serial output

  Reads an analog input pin, maps the result to a range from 0 to 255 and uses
  the result to set the pulse width modulation (PWM) of an output pin.
  Also prints the results to the Serial Monitor.

  The circuit:
  - potentiometer connected to analog pin 0.
    Center pin of the potentiometer goes to the analog pin.
    side pins of the potentiometer go to +5V and ground
  - LED connected from digital pin 9 to ground through 220 ohm resistor

  created 29 Dec. 2008
  modified 9 Apr 2012
  by Tom Igoe

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogInOutSerial
*/
#include <SPI.h>
#include <SD.h>
#include <string.h>

// set up variables using the SD utility library functions:
Sd2Card card;
SdVolume volume;
SdFile root;

File myFile;


// These constants won't change. They're used to give names to the pins used:
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
//const int analogOutPin = 9;  // Analog output pin that the LED is attached to

int ledPin = 6;

const int buttonPin = 2;
int buttonState = 0; 

int sensorValue = 0;  // value read from the pot
int outputValue = 0;  // value output to the PWM (analog out)

unsigned long second = 1000;
unsigned long previousMillis = 0;

//String wingfile = "wingbeat.txt";
String wingfile = "wingbeat.txt";

int file_count = 0;

void setup() {

  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);

  // initialize serial communications at 9600 bps:
  Serial.begin(9600);

  // while (!Serial) {
  //   ; // wait for serial port to connect. Needed for Leonardo only
  // }

  Serial.print("Initializing SD card...");

  if (!SD.begin()) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");

  //String wingfile = "wingbeat2.txt";

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  //myFile = SD.open(wingfile, FILE_WRITE);

  // if the file opened okay, write to it:
  // if (myFile) {
  //   String start_write = "Writing to " + wingfile;
  //   Serial.print(start_write);
  //   //myFile.println("testing 1, 2, 3.");
  //   // close the file:
  //   myFile.close();
  //   Serial.println(" done.");
  // } else {
  //   // if the file didn't open, print an error:
  //   String error_msg = "error opening " + wingfile;
  //   Serial.println(error_msg);
  // }

  // // re-open the file for reading:
  // myFile = SD.open(wingfile);
  // if (myFile) {
  //   Serial.println(wingfile);

  //   // read from the file until there's nothing else in it:
  //   while (myFile.available()) {
  //     Serial.write(myFile.read());
  //   }
  //   // close the file:
  //   myFile.close();
  // } else {
  //   // if the file didn't open, print an error:
  //   String error_msg = "error opening " + wingfile;
  //   Serial.println(error_msg);
  // }

  delay(second*5);

  Serial.println("Starting writing to SD");
}

int oldOutputValue = 0;
int count = 0;

int writeToSD = 1;

void loop() {

  unsigned long currentMillis = millis();  

  if(currentMillis - previousMillis >= second*30){
    previousMillis = currentMillis;
    writeToSD = 0;
  }


  if(writeToSD){
    //Serial.print(currentMillis);
    sensorValue = analogRead(analogInPin);
    // map it to the range of the analog out:
    outputValue = map(sensorValue, 0, 1023, 0, 255);
    // change the analog out value:
    //analogWrite(analogOutPin, outputValue);

    myFile = SD.open(wingfile, FILE_WRITE);
    Serial.println(wingfile);
    // if the file opened okay, write to it:
    if (myFile) {
      //String start_write = "Writing to " + wingfile;
      //Serial.print(start_write);
      myFile.println(sensorValue);
      // close the file:
      myFile.close();
      //Serial.println(" done.");
    } else {
      // if the file didn't open, print an error:
      String error_msg = "error opening " + wingfile;
      Serial.println(error_msg);
      myFile.close();
    }
  } else  {
    if(count == 0) {
      Serial.println("finished writing to SD");
      count++;
    }

    if(file_count < 1){
    
      file_count++;

      writeToSD = 1;
      wingfile = "wingbeat" + String(file_count) + ".txt";
      delay(second*5);
      String msg = "Starting " + wingfile;
      Serial.println(msg);

    } else if (file_count == 6) {
      Serial.println("Finished writing all files");
    }
      
  }

  
  delay(2);
}
