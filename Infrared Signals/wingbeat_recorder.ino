
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

int ledPin = 6;

const int buttonPin = 2;
int buttonState = 0; 

int sensorValue = 0;  // value read from the pot
int outputValue = 0;  // value output to the PWM (analog out)

unsigned long second = 1000;
unsigned long previousMillis = 0;



int file_count = 0;

void setup() {

  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);

  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  Serial.print("Initializing SD card...");
  if (!SD.begin()) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");
  delay(second*5);

  Serial.println("Starting writing to SD");
  Serial.println("Starting writing to SD");
  Serial.println("Starting writing to SD");
}

int oldOutputValue = 0;
int count = 0;

int writeToSD = 1;
String wingfile = "wingbeat.txt";

void loop() {

unsigned long currentMillis = millis();  

//checking if the interval has passed
//   if(currentMillis - previousMillis >= second*160){
//     previousMillis = currentMillis;
//     writeToSD = 0;
//   }

  sensorValue = analogRead(analogInPin);

  Serial.println(sensorValue);

  delay(2);



//   if(writeToSD){
 
//     sensorValue = analogRead(analogInPin);
//     // map it to the range of the analog out:
//     outputValue = map(sensorValue, 0, 1023, 0, 255);
//     myFile = SD.open(wingfile, FILE_WRITE);
//     if (myFile) {
//       myFile.println(sensorValue);
//       myFile.close();
//     } else {
//       // if the file didn't open, print an error:
//       String error_msg = "error opening " + wingfile;
//       Serial.println(error_msg);
//       myFile.close();
//     }
//   } else  {
//     if(file_count < 1){
//       file_count++;
//       writeToSD = 1;
//       wingfile = "wingbeat" + String(file_count) + ".txt";
//       delay(second*5);
//       String msg = "Starting " + wingfile;
//       Serial.println(msg);

//     } else if (file_count == 6) {
//       Serial.println("Finished writing all files");
//     }
      
//   }

  
  delay(2);
}
