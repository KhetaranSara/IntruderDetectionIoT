// UltrasonicSensor.h
#ifndef ULTRASONICSENSOR_H
#define ULTRASONICSENSOR_H

class UltrasonicSensor {
public:
    UltrasonicSensor(int pingPin, int inPin);
    void init();  // แทนการเริ่ม Serial.begin() แค่ setup ขาของเซนเซอร์
    long getDistance();

private:
    int _pingPin;
    int _inPin;
    long microsecondsToCentimeters(long microseconds);
};

#endif
