//
// Created by prostoichelovek on 14.04.2020.
//

#ifndef ARDU_INTERFACING_MANAGER_MESSAGEREADER_H
#define ARDU_INTERFACING_MANAGER_MESSAGEREADER_H


#include "Message/Message.h"
#include "Message/Symbols.h"
#include "utils.hpp"
#include <ArduinoSTL.h>

namespace Interfacing {

    class MessageReader {
    public:
        const std::string &current_node;

        Messages::Message msg;

        explicit MessageReader(const std::string &current_node);

        enum Status {
            MESSAGE_READY,
            MESSAGE_NOT_READY,
            MESSAGE_NOT_FOR_ME,
            INCORRECT_FORMAT
        };

        Status read(const char &symbol);

    private:
        void clear();

        bool message_started = false;
        bool header_started = false;
        bool parameters_started = false;
        int num_splitters = 0;
    };

}


#endif //ARDU_INTERFACING_MANAGER_MESSAGEREADER_H
