   #include <Wire.h>
#include "Seeed_BME280.h"
#include "SparkFun_Ublox_Arduino_Library.h"
#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#define LED_R 2
#define LED_G 3
#define LED_B 4
#define LED_LORA1 10
#define LED_LORA2 11
#define LED_RFD 12
#define LED_XBEE 13

SFE_UBLOX_GPS myGPS;
BME280 bme280;
Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28);

float TEMPERATURE = 0;
float PRESSURE = 0;
float ALTITUDE = 0;
float HUMIDITY = 0;
float LATITUDE = 0;
float LONGITUDE = 0;
float MAG_X = 0;
float MAG_Y = 0;
float MAG_Z = 0;
unsigned long time1=0;
unsigned long time0=0;

String G_Data = "";   //Ground's Data
String Serial_0 = ""; //Serial
String Serial_2 = ""; //lora1
String Serial_3 = ""; //lora2
String Serial_4 = ""; //rfd
String Serial_5 = ""; //xbee

void setup() {
  Serial.begin(9600); // Serial moniter
  Serial1.begin(9600);// Bluetooth
  Serial2.begin(9600);// LORA 1
  Serial3.begin(9600);// LORA 2
  Serial4.begin(9600);// RFD
  Serial5.begin(9600);// XBEE
  
  pinMode(LED_R,OUTPUT);
  pinMode(LED_G,OUTPUT);
  pinMode(LED_B,OUTPUT);
  pinMode(LED_LORA1,OUTPUT);
  pinMode(LED_LORA2,OUTPUT);
  pinMode(LED_RFD,OUTPUT);
  pinMode(LED_XBEE,OUTPUT);
  
  myGPS.begin();
  bme280.init();
  bno.begin();
  bno.setExtCrystalUse(true);
  myGPS.setI2COutput(COM_TYPE_UBX);
  myGPS.setNavigationFrequency(10); 
  
  digitalWrite(LED_LORA1,HIGH);   
  digitalWrite(LED_LORA2,HIGH);  
  digitalWrite(LED_R,HIGH);  
  digitalWrite(LED_G,HIGH);
  digitalWrite(LED_B,HIGH);   
  digitalWrite(LED_RFD,HIGH);   
  digitalWrite(LED_XBEE,HIGH);   
  digitalWrite(LED_G,HIGH);   
  digitalWrite(LED_G,HIGH);   
  delay(1000);
  digitalWrite(LED_LORA1,LOW);   
  digitalWrite(LED_LORA2,LOW);  
  digitalWrite(LED_R,LOW);  
  digitalWrite(LED_G,LOW);
  digitalWrite(LED_B,LOW);   
  digitalWrite(LED_RFD,LOW);   
  digitalWrite(LED_XBEE,LOW);   
  digitalWrite(LED_G,LOW);   
  digitalWrite(LED_G,LOW);


}

void get_BME(){
  TEMPERATURE = bme280.getTemperature();
  PRESSURE  = bme280.getPressure();
  ALTITUDE = bme280.calcAltitude(PRESSURE);
  HUMIDITY = bme280.getHumidity();
}

void get_GPS(){
  LATITUDE = myGPS.getLatitude();
  LONGITUDE = myGPS.getLongitude();
}

void get_BNO(){
  imu::Vector<3> MAG = bno.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER);
  MAG_X = MAG.x();
  MAG_Y = MAG.y();
  MAG_Z = MAG.z();
}
void Ground(){
    get_BME();
    get_BNO();
    get_GPS();
    G_Data = "G,"+String(LATITUDE,7)+","+String(LONGITUDE,7)+","+String(ALTITUDE)+","
    +String(MAG_X)+","+String(MAG_Y)+","+String(MAG_Z)+","+String(TEMPERATURE)+","+String(PRESSURE)+","+String(HUMIDITY);
    Serial.println(G_Data);
}
void BAT(){
    float a = analogRead(A9);
    if (a<=2){
      digitalWrite(LED_R,HIGH);
      digitalWrite(LED_G,LOW);
      digitalWrite(LED_B,LOW);
    }
    else if(a<=3){
      digitalWrite(LED_R,HIGH);
      digitalWrite(LED_G,HIGH);
      digitalWrite(LED_B,HIGH);
    }
    else{
      digitalWrite(LED_G,HIGH);
      digitalWrite(LED_R,LOW);
      digitalWrite(LED_B,LOW);
    }
}

void loop(){
//    BAT();
//    time1 = millis();
//    if (time1-time0>=990){
////      Ground();
//      time0=millis();
//    }
//    while(Serial.available()){
//      Serial_0 = Serial.readStringUntil('$');
//      Serial_0.trim();
//    }
    
    if(Serial2.available()){
       Serial_2 = Serial2.readStringUntil('$');
       Serial.println(Serial_2+String('$'));
       digitalWrite(LED_LORA1,HIGH);
    }
    if(Serial3.available()){
       Serial_3 = Serial3.readStringUntil('\n');
       Serial.println(Serial_3+String('$'));
       digitalWrite(LED_LORA2,HIGH);
    }
//    if(Serial4.available()){
//       Serial_4 = Serial4.readStringUntil('$');
//       Serial.println(Serial_4+String('$'));
//       digitalWrite(LED_RFD,HIGH);
//    }
//    if(Serial5.available()){
//       Serial_5 = Serial5.readStringUntil('$');
//       Serial.println(Serial_5+String('$'));
//       digitalWrite(LED_XBEE,HIGH);
//    }
    digitalWrite(LED_LORA1,LOW);    
    digitalWrite(LED_LORA2,LOW);
    digitalWrite(LED_RFD,LOW);    
    digitalWrite(LED_RFD,LOW);
    
}
