//
// Created by prostoichelovek on 15.04.2020.
//

#include "InterfacingManager/SerialBridge.h"

namespace Interfacing {

    SerialBridge::SerialBridge() = default;

    void SerialBridge::send(const std::string &data) {
        Serial.println(data.c_str());
    }

    char SerialBridge::read() {
        return Serial.read();
    }

    bool SerialBridge::available() {
        return Serial.available() > 0;
    }

    void SerialBridge::flush() {
        for (int i = 0; i < 10; ++i) {
            while (Serial.available() > 0) {
                Serial.read();
                delay(7);
            }
            delay(7);
        }
    }

}