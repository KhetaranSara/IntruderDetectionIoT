#define BLYNK_PRINT Serial

/* Fill in information from Blynk Device Info here */
#define BLYNK_TEMPLATE_ID "TMPL6-fpg-Gqk"
#define BLYNK_TEMPLATE_NAME "capture"
#define BLYNK_AUTH_TOKEN "RmNVvsKZRg7EbeFWzSH-oSTiBLgFVWke"
#include "Servo.h"


#include <Arduino.h>
#include <WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
#include <BlynkSimpleWifi.h>
#include <SPI.h>
#include "AudioPlayer.h"
#include "UltrasonicSensor.h"
#include <BlynkSimpleWifi.h>
#include <TimeLib.h>
// MQTT SETTING
#define AIO_USERNAME "65050101"
#define AIO_KEY "aio_rtaT32P6zBe87LXT5Iz9fsrjFrkB"
#define servo7 7
const char *ssid = "peepeeza";
const char *password = "Kukurubo12345.";
const int ledPin = 13;
BlynkTimer timer;
WiFiClient client;

Adafruit_MQTT_Client mqtt(&client, "io.adafruit.com", 1883, AIO_USERNAME, AIO_KEY);
Adafruit_MQTT_Subscribe matchFace_feed(&mqtt, AIO_USERNAME "/feeds/matchFace");
Adafruit_MQTT_Publish ultrasonic_feed(&mqtt, AIO_USERNAME "/feeds/ultrasonic");
Servo myservo;
// SENSOR SETTING
//RedGreenLED led(13, 5);
AudioPlayer sound(2, 3);
UltrasonicSensor sensor(10,11);

long cm;

BLYNK_CONNECTED() {
  Blynk.sendInternal("rtc", "sync"); // ส่งคำสั่งขอเวลาไปยัง Blynk RTC Widget
}

BLYNK_WRITE(InternalPinRTC) {
  long unixTime = param.asLong(); // ดึงค่า Unix Time จาก Blynk
  setTime(unixTime); // ตั้งเวลาใน TimeLib
  Serial.print("Unix time synced: ");
  Serial.println(unixTime);

  Serial.print("Current time: ");
  Serial.print(hour());
  Serial.print(":");
  Serial.print(minute());
  Serial.print(":");
  Serial.println(second());
}

void checkLedControl() {
  if (hour() == 7 && minute() == 30) { // เมื่อถึงเวลา 20:30
    digitalWrite(ledPin, HIGH); // เปิดไฟ LED
    Serial.println("LED turned ON at 7:30");
  }
  else if (hour() == 10 && minute() == 00) { // เมื่อถึงเวลา 20:30
    digitalWrite(ledPin, LOW); // เปิดไฟ LED
  }

  if (hour() == 18 && minute() == 30) { // เมื่อถึงเวลา 20:30
    digitalWrite(ledPin, HIGH); // เปิดไฟ LED
    Serial.println("LED turned ON at 18:30");
  }
  else if (hour() == 21 && minute() == 30) { // เมื่อถึงเวลา 20:30
    digitalWrite(ledPin, LOW); // เปิดไฟ LED
  }

  if (hour() == 23 && minute() == 30) { // เมื่อถึงเวลา 20:30
    digitalWrite(ledPin, HIGH); // เปิดไฟ LED
    Serial.println("LED turned ON for Intruder");
  }
  else if (hour() == 5 && minute() == 00) { // เมื่อถึงเวลา 20:30
    digitalWrite(ledPin, LOW); // เปิดไฟ LED
  }
}

void setup() {
  
  Serial.begin(9600);
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, password);
  // MQTT CONNECTION
  WiFi_connect();
  mqtt.subscribe(&matchFace_feed);
  // SET UP SENSOR
  sound.begin();
  sound.setVolume(30);
  sensor.init();
  
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  timer.setInterval(10000L, checkLedControl);
}

void WiFi_connect() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
}

void loop() {
  MQTT_connect();
  cm = sensor.getDistance();
  Serial.print(cm);
  Serial.println(" cm");
  if(cm <= 30){
    ultrasonic_feed.publish("1");
  }else{
    ultrasonic_feed.publish("0");
  }
  delay(5000);
  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(2000))) {
    if (subscription == &matchFace_feed) {
      Serial.print("Received : ");
      Serial.print((char *)matchFace_feed.lastread);

      if (strcmp((char *)matchFace_feed.lastread, "0") == 0) {
        Serial.println(" :Nothing to Do.");
      } else if (strcmp((char *)matchFace_feed.lastread, "1") == 0) {
        Serial.println(" :Found host.");

        Serial.println("Unlock the Door.");
      } else {
        Serial.println(" :พบผู้บุกรุก");
        Serial.println("ทำการเล่นเสียงหลอก");
        sound.playDoorBell();
        delay(2000);
        sound.playGreetingMessage();
      }
    }
  }
  
  Blynk.run();
  timer.run();
}

void MQTT_connect() {
  int8_t ret;
  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");

  while ((ret = mqtt.connect()) != 0) {  // เชื่อมต่อไม่ได้
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println(" Retrying in 5 seconds...");
    mqtt.disconnect();
    delay(5000);  // รอ 5 วินาทีเพื่อเชื่อมต่อใหม่
  }
  Serial.println("MQTT Connected!");
}
// BLYNK_WRITE(V5) {  //MEDICINE MODE SELECT
//   int disallow = param.asInt();
//   if(disallow == 1){
//     Serial.println("disallowPress");
//     sound.playGreetingMessage();
//   }

// }
BLYNK_WRITE(V6) {  //MEDICINE MODE SELECT
  int allow = param.asInt();
if (allow == 1) {
    Serial.println("allowPress");
    
    // เริ่มต้นการเชื่อมต่อ Servo กับพินที่ต้องการ
    myservo.attach(servo7);
    
    // ตั้งค่ามุมเริ่มต้น
    myservo.write(0);
    delay(1000); // หน่วงเวลา 1 วินาทีเพื่อให้ Servo อยู่ในตำแหน่งเริ่มต้น

    // หมุน Servo ไปที่ 90 องศาเพื่อเปิดกลอน
    myservo.write(90);
    delay(5000); // หน่วงเวลา 5 วินาทีเพื่อเปิดกลอน

    // หมุน Servo กลับไปที่ 0 องศาเพื่อปิดกลอน
    myservo.write(0);
    delay(1000); // หน่วงเวลา 1 วินาทีเพื่อให้ Servo ปิดกลอน

    // ปลดการเชื่อมต่อ Servo เพื่อหยุดการทำงาน
    myservo.detach();
}

}
