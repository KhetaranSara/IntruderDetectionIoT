#include "esp_camera.h"
#include <WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
#include <WiFiClientSecure.h>
#include <TridentTD_LineNotify.h>
#include <Arduino.h>

#define AIO_USERNAME "65050101"
#define AIO_KEY "xxxxxxxxxxxx"

#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"
#define FLASH_PIN 4

const char* ssid = "peepeeza";
const char* password = "Kukurubo12345.";
const char* LINE_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxx";

WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, "io.adafruit.com", 1883, AIO_USERNAME, AIO_KEY);

// Define separate variables for publishing and subscribing
//Adafruit_MQTT_Publish ultrasonic_publish = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/ultrasonic");
Adafruit_MQTT_Subscribe matchFace_feed(&mqtt, AIO_USERNAME "/feeds/matchFace");
Adafruit_MQTT_Subscribe ultrasonic_subscribe(&mqtt, AIO_USERNAME "/feeds/ultrasonic");

void setup() {
  Serial.begin(9600);
  pinMode(FLASH_PIN, OUTPUT);
  digitalWrite(FLASH_PIN, LOW);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  // Set LINE Notify token
  LINE.setToken(LINE_TOKEN);

  // Camera setup code
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

  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera init failed!");
    return;
  }

  // Subscribe to feeds
  mqtt.subscribe(&matchFace_feed);
  mqtt.subscribe(&ultrasonic_subscribe);
}

  void loop() {
    if (!mqtt.connected()) MQTT_connect();
    Adafruit_MQTT_Subscribe* subscription;

    // Read subscriptions
    while ((subscription = mqtt.readSubscription(3000))) {
      if (subscription == &matchFace_feed || subscription == &ultrasonic_subscribe) {
        Serial.print("Received MatchFace: ");
        Serial.println((char*)matchFace_feed.lastread);
        Serial.print("Received ultrasonic status: ");
        Serial.println((char*)ultrasonic_subscribe.lastread);
        if (strcmp((char*)matchFace_feed.lastread, "-1") == 0 && strcmp((char*)ultrasonic_subscribe.lastread, "1") == 0) {
          Serial.println(" Intruder detected!");
          Serial.println("Send notification to LINE!");
          LINE.notify("Intruder detected!");
          Camera_capture();
        }
      }
      delay(1000);
    }
    delay(7000);
}

void MQTT_connect() {
  while (mqtt.connect() != 0) {
    Serial.println("MQTT connection failed! Retrying...");
    delay(2000);
  }
  Serial.println("MQTT connected.");
}

void Camera_capture() {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }
  Send_line(fb->buf, fb->len);
  esp_camera_fb_return(fb);
}

void Send_line(uint8_t* image_data, size_t image_size) {
  LINE.notifyPicture("Intruder Alert!", image_data, image_size);
  Serial.println("Picture sent to LINE Notify");
}
