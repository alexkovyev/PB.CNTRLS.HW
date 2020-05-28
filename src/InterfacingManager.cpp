//
// Created by prostoichelovek on 15.04.2020.
//

#include "InterfacingManager/InterfacingManager.h"

namespace Interfacing {

    InterfacingManager::InterfacingManager(const std::string &current_node)
            : current_node(current_node), reader(this->current_node) {
    }

    MessageReader::Status InterfacingManager::update() {
        if (bridge.available()) {
            char sym = bridge.read();
            MessageReader::Status status = reader.read(sym);
            if (status == MessageReader::MESSAGE_NOT_FOR_ME || status == MessageReader::INCORRECT_FORMAT) {
                bridge.flush();
            } else if (status == MessageReader::MESSAGE_READY) {
                if (!validators(reader.msg)) {
                    return MessageReader::INCORRECT_FORMAT;
                }
            }
            return status;
        }
        return MessageReader::MESSAGE_NOT_READY;
    }

    Messages::Message &InterfacingManager::get_massage() {
        return reader.msg;
    }

    void InterfacingManager::send_message(const Messages::Message &msg) {
        bridge.send(msg.to_string());
    }

}
