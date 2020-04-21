//
// Created by prostoichelovek on 14.04.2020.
//

#include "InterfacingManager/MessageReader.h"

namespace Interfacing {

    MessageReader::MessageReader(const std::string &current_node)
            : current_node(current_node) {
    }

    MessageReader::Status MessageReader::read(const char &symbol) {
        if (symbol == '\n' && message_started) {
            goto format_error; // goto is not always a bad practice
        } else if (symbol == Messages::start_sym) {
            message_started = !message_started;
            if (!message_started) { // message finished
                if (parameters_started) { // message is finished, but no parameters ending symbol was presented
                    goto format_error;
                }
                if (num_splitters == 0) {
                    goto format_error;
                }
                return MessageReader::Status::MESSAGE_READY;
            } else { // message started
                clear();
                message_started = true; // clear sets it to false
            }
        } else if (message_started) {
            if (symbol == Messages::header_start_sym) {
                if (parameters_started) { // header should be before parameters
                    goto format_error;
                }
                header_started = true;
            } else if (symbol == Messages::header_end_sym) {
                if (!header_started) { // header finishing symbol before header started
                    goto format_error;
                }
                if (num_splitters != 1) { // there should be one splitter within the header
                    goto format_error;
                }
                header_started = false;
            } else if (symbol == Messages::parameters_start_sym) {
                if (header_started) { // no header finishing symbol before parameters
                    goto format_error;
                }
                parameters_started = true;
                msg.parameters.push_back("");
            } else if (symbol == Messages::parameters_end_sym) {
                if (!parameters_started) { // parameters finishing symbol before parameters started
                    goto format_error;
                }
                parameters_started = false;
            } else if (symbol == Messages::splitter_sym) {
                num_splitters++;
                if (parameters_started) {
                    msg.parameters.push_back("");
                } else if (!header_started) { // splitter before message body
                    goto format_error;
                } else { // header started
                    if (msg.node_name != current_node) {
                        clear();
                        return MESSAGE_NOT_FOR_ME;
                    }
                }
            } else { // service symbols won`t be included in the message
                if (header_started) {
                    if (num_splitters == 0) {
                        msg.node_name += symbol;
                    } else {
                        msg.command_name += symbol;
                    }
                } else if (parameters_started) {
                    msg.parameters.back() += symbol;
                }
            }
        }

        return MessageReader::Status::MESSAGE_NOT_READY;

        format_error:
        {
            /*
            Serial.println("Incorrect format:");
            msg.print_serial();
            Serial.print("Symbol: '");
            Serial.print(symbol);
            Serial.println("'");
            */

            clear();
            return MessageReader::Status::INCORRECT_FORMAT;
        };
    }

    void MessageReader::clear() {
        message_started = false;
        header_started = false;
        parameters_started = false;
        num_splitters = 0;
        msg.clear();
    }

}
