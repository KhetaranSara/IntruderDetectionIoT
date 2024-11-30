// UltrasonicSensor.cpp
#include "UltrasonicSensor.h"
#include <Arduino.h>

UltrasonicSensor::UltrasonicSensor(int pingPin, int inPin)
    : _pingPin(pingPin), _inPin(inPin) {}

void UltrasonicSensor::init() {
    // ไม่มี Serial.begin() ในนี้
}

long UltrasonicSensor::getDistance() {
    long duration, cm;
    pinMode(_pingPin, OUTPUT);
    digitalWrite(_pingPin, LOW);
    delayMicroseconds(2);
    digitalWrite(_pingPin, HIGH);
    delayMicroseconds(5);
    digitalWrite(_pingPin, LOW);

    pinMode(_inPin, INPUT);
    duration = pulseIn(_inPin, HIGH);
    cm = microsecondsToCentimeters(duration);

    return cm;
}

long UltrasonicSensor::microsecondsToCentimeters(long microseconds) {
    return microseconds / 29 / 2;
}
