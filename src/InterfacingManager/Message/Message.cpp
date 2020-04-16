//
// Created by prostoichelovek on 14.04.2020.
//

#include <InterfacingManager/utils.hpp>
#include "Message.h"
#include "Symbols.h"

namespace Interfacing {
    namespace Messages {

        Message::Message(Message &other) {
            node_name = other.node_name;
            command_name = other.command_name;
            parameters = other.parameters;
        }

        Message::Message(const std::string &nodeName, const std::string &commandName,
                         const std::vector<std::string> &parameters) : node_name(nodeName), command_name(commandName),
                                                                       parameters(parameters) {}

        Message &Interfacing::Messages::Message::operator=(Interfacing::Messages::Message &&other) noexcept {
            if (this != &other) {
                node_name = other.node_name;
                command_name = other.command_name;
                parameters = other.parameters;
            }
            return *this;
        }

        void Message::print_serial() {
            std::cout << "Message: {" << std::endl;
            std::cout << "\tNode name: " << node_name << std::endl;
            std::cout << "\tCommand name: " << command_name << std::endl;
            Serial.println("\tParameters: [");
            for (const auto &param : parameters) {
                std::cout << "\t\t" << param << std::endl;
            }
            std::cout << "\t]\n}" << std::endl;
        }

        std::string Message::to_string() {
            std::string header = header_start_sym + node_name + splitter_sym + command_name + header_end_sym;
            std::string params_str;
            for (const auto &param : parameters) {
                params_str += param + splitter_sym;
            }
            if (!parameters.empty()) {
                params_str.pop_back();
            }

            return start_sym + header + parameters_start_sym + params_str + parameters_end_sym + end_sym;
        }

        void Message::clear() {
            node_name = "";
            command_name = "";
            parameters.clear();
        }

    }
}