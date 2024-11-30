#include "AudioPlayer.h"

AudioPlayer::AudioPlayer(int rxPin, int txPin) 
    : mySoftwareSerial(rxPin, txPin) {
}

void AudioPlayer::begin() {
    mySoftwareSerial.begin(9600);
    Serial.begin(9600);

    Serial.println();
    Serial.println(F("DFRobot DFPlayer Mini Demo"));
    Serial.println(F("Initializing DFPlayer ... (May take 3~5 seconds)"));

    if (!myDFPlayer.begin(mySoftwareSerial)) {
        Serial.println(F("Unable to begin:"));
        Serial.println(F("1. Please recheck the connection!"));
        Serial.println(F("2. Please insert the SD card!"));
        while (true) {
            delay(0);
        }
    }
    Serial.println(F("DFPlayer Mini online."));
}

void AudioPlayer::playDoorBell() {
    myDFPlayer.play(1);
}

void AudioPlayer::playGreetingMessage() {
    myDFPlayer.play(2);
}

void AudioPlayer::stop() {
    myDFPlayer.stop();
}

void AudioPlayer::setVolume(uint8_t volume) {
    myDFPlayer.volume(volume); // ระดับความดังของเสียง 0-30
}
