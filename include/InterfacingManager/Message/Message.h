//
// Created by prostoichelovek on 14.04.2020.
//

#ifndef ARDU_INTERFACING_MANAGER_MESSAGE_H
#define ARDU_INTERFACING_MANAGER_MESSAGE_H


#include <Arduino.h>
#include <ArduinoSTL.h>

namespace Interfacing {
    namespace Messages {

        class Message {
        public:
            std::string node_name;
            std::string command_name;
            std::vector<std::string> parameters;

            Message() = default;

            Message(const std::string &nodeName, const std::string &commandName,
                    const std::vector<std::string> &parameters);

            Message(const std::string &nodeName, const std::string &commandName);

            Message(const Message &other);

            void print_serial();

            void clear();

            std::string to_string();

            Message &operator=(Message &&other) noexcept;
        };

    }
}


#endif //ARDU_INTERFACING_MANAGER_MESSAGE_H
