//
// Created by prostoichelovek on 15.04.2020.
//

#ifndef ARDU_INTERFACING_MANAGER_SERIALBRIDGE_H
#define ARDU_INTERFACING_MANAGER_SERIALBRIDGE_H


#include <Arduino.h>
#include "utils.hpp"

namespace Interfacing {

    class SerialBridge {
    public:
        SerialBridge();

        void send(const std::string &data);

        char read();

        bool available();

        void flush();
    };

}


#endif //ARDU_INTERFACING_MANAGER_SERIALBRIDGE_H
