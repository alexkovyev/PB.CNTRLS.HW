//
// Created by prostoichelovek on 14.04.2020.
//

#ifndef ARDU_INTERFACING_MANAGER_UTILS_HPP
#define ARDU_INTERFACING_MANAGER_UTILS_HPP

#include <ArduinoSTL.h>
#include <ArduinoSTL.h>

namespace Interfacing {

    inline void flush_serial() {
        for (int i = 0; i < 10; ++i) {
            while (Serial.available() > 0) {
                Serial.read();
                delay(7);
            }
            delay(7);
        }
    }

    inline int availableMemory() {
        // Use 1024 with ATmega168
        int size = 2048;
        byte *buf;
        while ((buf = (byte *) malloc(--size)) == NULL);
        free(buf);
        return size;
    }

    // https://stackoverflow.com/a/4654718/9577873
    inline bool is_number(const std::string &s) {
        auto it = s.begin();
        while (it != s.end() && std::isdigit(*it)) ++it;
        return !s.empty() && it == s.end();
    }

    // https://stackoverflow.com/a/19751887/9577873
    static bool isFloatNumber(const std::string &string) {
        auto it = string.begin();
        bool decimalPoint = false;
        int minSize = 0;
        if (!string.empty() && (string[0] == '-' || string[0] == '+')) {
            it++;
            minSize++;
        }
        while (it != string.end()) {
            if (*it == '.') {
                if (!decimalPoint) decimalPoint = true;
                else break;
            } else if (!std::isdigit(*it) && ((*it != 'f') || it + 1 != string.end() || !decimalPoint)) {
                break;
            }
            ++it;
        }
        return string.size() > minSize && it == string.end();
    }

}

#endif //ARDU_INTERFACING_MANAGER_UTILS_HPP
