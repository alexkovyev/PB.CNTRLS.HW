//
// Created by prostoichelovek on 13.04.2020.
//

#include <Arduino.h>
#include "InterfacingManager/InterfacingManager.h"
#include "InterfacingManager/ParametersValidator.h"

using namespace Interfacing;

InterfacingManager manager("Dispenser");

void setup() {
    Serial.begin(9600);
    const auto name_validator = ParametersValidator([](const std::string &param) -> bool {
        return !param.empty();
    }, 0);
    const auto rgb_validator = ParametersValidator([](const std::string &param) -> bool {
        return param == "0" || param == "1";
    }, 1, 3);
    const auto min_max_validator = ParametersValidator([](const std::string &param) -> bool {
        if (!is_number(param)) {
            return false;
        }
        int param_num = atoi(param.c_str());
        return param_num >= 0 && param_num <= 255;
    }, 4, 5);
    const auto seconds_validator = ParametersValidator([](const std::string &param) -> bool {
        if (!isFloatNumber(param)) {
            return false;
        }
        return atof(param.c_str()) >= 0;
    }, 6, 10);

    manager.validators.add("add_light_mode", std::vector<ParametersValidator>{
            name_validator, rgb_validator, min_max_validator, seconds_validator
    });
}

void loop() {
    auto status = manager.update();
    if (status == Interfacing::MessageReader::MESSAGE_READY) {
        manager.send_message(manager.get_massage());
    } else if (status == Interfacing::MessageReader::INCORRECT_FORMAT) {
        std::cout << "Incorrect format" << std::endl;
    }
}