#ifndef AUDIOPLAYER_H
#define AUDIOPLAYER_H

#include <Arduino.h>
#include <SoftwareSerial.h>
#include "DFRobotDFPlayerMini.h"

class AudioPlayer {
public:
    AudioPlayer(int rxPin, int txPin);
    void begin();
    void playDoorBell();
    void playGreetingMessage();
    void stop();
    void setVolume(uint8_t volume);

private:
    SoftwareSerial mySoftwareSerial;
    DFRobotDFPlayerMini myDFPlayer;
};

#endif
