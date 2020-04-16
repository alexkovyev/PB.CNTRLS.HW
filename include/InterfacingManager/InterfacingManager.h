//
// Created by prostoichelovek on 15.04.2020.
//

#ifndef ARDU_INTERFACING_MANAGER_INTERFACINGMANAGER_H
#define ARDU_INTERFACING_MANAGER_INTERFACINGMANAGER_H


#include "MessageReader.h"
#include "SerialBridge.h"
#include "ValidatorsContainer.h"

namespace Interfacing {

    class InterfacingManager {
    public:
        const std::string current_node;

        SerialBridge bridge;
        MessageReader reader;
        ValidatorsContainer validators;

        explicit InterfacingManager(const std::string &current_node);

        MessageReader::Status update();

        Messages::Message &get_massage();

        void send_message(Messages::Message &msg);

    };

}

#endif //ARDU_INTERFACING_MANAGER_INTERFACINGMANAGER_H
