#include "esp_camera.h"
#include <WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

#define AIO_USERNAME "65050101"                     // ใส่ Adafruit IO Username ของคุณ
#define AIO_KEY "aio_rtaT32P6zBe87LXT5Iz9fsrjFrkB"  // ใส่ Adafruit IO Key ของคุณ
#define CAMERA_MODEL_AI_THINKER

#include "camera_pins.h"

// WiFi และ Adafruit IO Config
// const char* ssid = "PPNET-2.4G";
// const char* password = "k0939911535";

const char* ssid = "peepeeza";
const char* password = "Kukurubo12345.";

WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, "io.adafruit.com", 1883, AIO_USERNAME, AIO_KEY);

// Feed สำหรับการส่งข้อมูล matchFace
Adafruit_MQTT_Publish matchFace_feed = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/matchFace");

int matchFace = 0;

void startCameraServer();

void setup() {
  Serial.begin(9600);
  Serial.setDebugOutput(true);
  Serial.println();

  // ตั้งค่ากล้อง
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

  // ตรวจสอบ PSRAM
  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t* s = esp_camera_sensor_get();
  //initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1);        //flip it back
    s->set_brightness(s, 1);   //up the blightness just a bit
    s->set_saturation(s, -2);  //lower the saturation
  }
  //drop down frame size for higher initial frame rate
  s->set_framesize(s, FRAMESIZE_QVGA);

#if defined(CAMERA_MODEL_M5STACK_WIDE)
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);
#endif

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  startCameraServer();

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");
}

void loop() {
  // ตรวจสอบการเชื่อมต่อกับ MQTT
  MQTT_connect();
    if (matchFace == -1 || matchFace == 1) {
      if (!matchFace_feed.publish(matchFace)) {
        matchFace_feed.publish(matchFace);
        Serial.println("Failed to publish matchFace");
      } else {
        Serial.println("matchFace sent to Adafruit IO");
      }
      delay(10000);
      matchFace = 0;
      if (!matchFace_feed.publish(matchFace)) {
        matchFace_feed.publish(matchFace);
        Serial.println("Failed to publish matchFace");
      } else {
        Serial.println("matchFace sent to Adafruit IO");
      }
    } 
    delay(10000);  
}

// ฟังก์ชันเชื่อมต่อกับ MQTT
void MQTT_connect() {
  int8_t ret;

  // ลองเชื่อมต่อกับ MQTT
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