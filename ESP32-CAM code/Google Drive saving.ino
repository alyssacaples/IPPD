// Enter your WiFi ssid and password
const char* ssid     = "Adam_iPhone";   //your network SSID
const char* password = "ixg2pot2qd691";   //your network password
//const char* ssid     = "";   //your network SSID
//const char* password = "";   //your network password

String myScript = "/macros/s/AKfycbyqkBmG-2DG1GjpVwpL0cepxmOdrdejhOuRFSScoJwIZj0LQvc8DxguyAodCoIkd3Bs4Q/exec";    //Create your Google Apps Script and replace the "myScript" path.
String myLineNotifyToken = "myToken=**********";    //Line Notify Token. You can set the value of xxxxxxxxxx empty if you don't want to send picture to Linenotify.
String myFoldername = "&myFoldername=ESP32-CAM";
String myFilename = "&myFilename=ESP32-CAM.jpg";
String myImage = "&myFile=";

uint8_t timer_done = 0;
hw_timer_t* timeout_timer = nullptr;

#include <WiFi.h>
#include <WiFiClientSecure.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "Base64.h"
#include <String.h>

#include "esp_camera.h"

// WARNING!!! Make sure that you have either selected ESP32 Wrover Module,
//            or another board which has PSRAM enabled

//CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

#define FLASH_GPIO_NUM 4

void IRAM_ATTR onTimer()
{
  timer_done = 1;
}

void setup()
{
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  
  Serial.begin(115200);
  delay(10);

  //set GPIO2 as input
  pinMode(2, INPUT);
  
  WiFi.mode(WIFI_STA);

  Serial.println("");
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);  
  
  long int StartTime=millis();
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    if ((StartTime+10000) < millis()) break;
  } 

  Serial.println("");
  Serial.println("STAIP address: ");
  Serial.println(WiFi.localIP());
    
  Serial.println("");
  pinMode(FLASH_GPIO_NUM, OUTPUT);
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Reset");
    
    /*ledcAttachPin(4, 3);
    ledcSetup(3, 5000, 8);
    ledcWrite(3,10);*/
    digitalWrite(FLASH_GPIO_NUM, HIGH);
    delay(200);
    //ledcWrite(3,0);
    digitalWrite(FLASH_GPIO_NUM, LOW);
    delay(200);    
    //ledcDetachPin(3);
        
    delay(1000);
    ESP.restart();
  }
  else {
    //ledcAttachPin(4, 3);
    //ledcSetup(3, 5000, 8);
    for (int i=0;i<5;i++) {
      //ledcWrite(3,10);
      digitalWrite(FLASH_GPIO_NUM, HIGH);
      delay(200);
      //ledcWrite(3,0);
      digitalWrite(FLASH_GPIO_NUM, LOW);
      delay(200);    
    }
    //ledcDetachPin(3);      
  }

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  //init with high specs to pre-allocate larger buffers
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;  //0-63 lower number means higher quality
    //config.jpeg_quality = 6;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;  //0-63 lower number means higher quality
    config.fb_count = 1;
  }
  
  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    delay(1000);
    ESP.restart();
  }

  //drop down frame size for higher initial frame rate
  sensor_t * s = esp_camera_sensor_get();
  //s->set_framesize(s, FRAMESIZE_VGA);  // UXGA|SXGA|XGA|SVGA|VGA|CIF|QVGA|HQVGA|QQVGA
  s->set_framesize(s, FRAMESIZE_QSXGA);

  Serial.println("Timer started");
  timeout_timer = timerBegin(0, 80, true);
  timerAttachInterrupt(timeout_timer, &onTimer, true);
  timerAlarmWrite(timeout_timer, 120000000, true);
  timerAlarmEnable(timeout_timer);
}

void take_picture()
{
  //ledcWrite(3,10);
  digitalWrite(FLASH_GPIO_NUM, HIGH);
  delay(1000);
  SendCapturedImage();
  delay(200);
  //ledcWrite(3,0);
  digitalWrite(FLASH_GPIO_NUM, LOW);
}

void loop()
{
  uint8_t button_pressed = 0;
  while (!button_pressed && !timer_done)
  {
    button_pressed = digitalRead(2);
    delay(10);
  }
  //do the following if timer has run out
  if (timer_done)
  {
    Serial.println("Timer has expired. Taking picture automatically.");
    for (uint8_t i = 0; i < 3; i++)
    {
      //ledcWrite(3,10);
      digitalWrite(FLASH_GPIO_NUM, HIGH);
      delay(200);
      //ledcWrite(3,0);
      digitalWrite(FLASH_GPIO_NUM, LOW);
      delay(200);    
    }
    take_picture();
    Serial.println("Going to sleep now");
    esp_sleep_enable_timer_wakeup(60 * 60 * 1000000);
    Serial.flush();
    esp_deep_sleep_start();
  }
  take_picture();
  timerRestart(timeout_timer);
  timer_done = 0;
  //delay(12000);
}

String SendCapturedImage() {
  const char* myDomain = "script.google.com";
  String getAll="", getBody = "";
  
  camera_fb_t * fb = NULL;
  fb = esp_camera_fb_get();  
  if(!fb) {
    Serial.println("Camera capture failed");
    delay(1000);
    ESP.restart();
    return "Camera capture failed";
  }  
  
  Serial.println("Connect to " + String(myDomain));
  WiFiClientSecure client_tcp;
  client_tcp.setInsecure();   //run version 1.0.5 or above
  
  if (client_tcp.connect(myDomain, 443)) {
    Serial.println("Connection successful");
    
    //crop_image(fb, 500, 500, 400, 400);
    char *input = (char *)fb->buf;
    char output[base64_enc_len(3)];
    //String imageFile = "data:image/jpeg;base64,";
    String init_image_data = "data:image/jpeg;base64,";
    int image_file_length = init_image_data.length();
    //first determine how long the base64 encoded image is
    for (int i=0;i<fb->len;i++) {
      base64_encode(output, (input++), 3);
      if (i%3==0)
      {
        //imageFile += urlencode(String(output));
        image_file_length += urlencode(String(output)).length();
      }
    }
    //this is metadata with a fixed length. all these variables are defined above.
    String Data = myLineNotifyToken+myFoldername+myFilename+myImage;

    Serial.println(image_file_length);
    //Serial.println(imageFile.length());    
    client_tcp.println("POST " + myScript + " HTTP/1.1");
    client_tcp.println("Host: " + String(myDomain));
    client_tcp.println("Content-Length: " + String(Data.length()+image_file_length));
    client_tcp.println("Content-Type: application/x-www-form-urlencoded");
    client_tcp.println("Connection: keep-alive");
    client_tcp.println();
    
    client_tcp.print(Data);
    client_tcp.print(init_image_data);

    input = (char *)fb->buf;
    String packet_string = "";
    for (int i=0;i<image_file_length;i++) {
      base64_encode(output, (input++), 3);
      if (i%3==0)
      {
        packet_string += urlencode(String(output));
      }
      if (i%1200==0)
      {
        //Serial.println(packet_string.length());
        client_tcp.print(packet_string);
        packet_string = "";
      }
      
    }
    client_tcp.print(packet_string);
    /*for (int i = 0; i < imageFile.length(); i = i+1000) {
      client_tcp.print(imageFile.substring(i, i+1000));
    }*/
    esp_camera_fb_return(fb);
    
    int waitTime = 10000;   // timeout 10 seconds
    long startTime = millis();
    boolean state = false;
    
    while ((startTime + waitTime) > millis())
    {
      Serial.print(".");
      delay(100);      
      while (client_tcp.available()) 
      {
          char c = client_tcp.read();
          if (state==true) getBody += String(c);        
          if (c == '\n') 
          {
            if (getAll.length()==0) state=true; 
            getAll = "";
          } 
          else if (c != '\r')
            getAll += String(c);
          startTime = millis();
       }
       if (getBody.length()>0) break;
    }
    client_tcp.stop();
    Serial.println(getBody);
  }
  else {
    getBody="Connected to " + String(myDomain) + " failed.";
    Serial.println("Connected to " + String(myDomain) + " failed.");
  }
  
  return getBody;
}


String urlencode(String str)
{
    String encodedString="";
    char c;
    char code0;
    char code1;
    char code2;
    for (int i =0; i < str.length(); i++){
      c=str.charAt(i);
      if (c == ' '){
        encodedString+= '+';
      } else if (isalnum(c)){
        encodedString+=c;
      } else{
        code1=(c & 0xf)+'0';
        if ((c & 0xf) >9){
            code1=(c & 0xf) - 10 + 'A';
        }
        c=(c>>4)&0xf;
        code0=c+'0';
        if (c > 9){
            code0=c - 10 + 'A';
        }
        code2='\0';
        encodedString+='%';
        encodedString+=code0;
        encodedString+=code1;
        //encodedString+=code2;
      }
      yield();
    }
    return encodedString;
}