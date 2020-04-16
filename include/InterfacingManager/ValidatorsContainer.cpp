//
// Created by prostoichelovek on 16.04.2020.
//

#include "ValidatorsContainer.h"

namespace Interfacing {


    void ValidatorsContainer::add(const std::string &command, const ParametersValidator &validator) {
        if (!validators.has_key(command)) {
            validators[command] = std::vector<ParametersValidator>{};
        }
        validators[command].push_back(validator);
    }

    void ValidatorsContainer::add(const std::string &command, const std::vector<ParametersValidator> &vals) {
        if (!validators.has_key(command)) {
            validators[command] = std::vector<ParametersValidator>{};
        }
        auto &current_validators = validators[command];
        current_validators.insert(current_validators.end(), vals.begin(), vals.end());
    }

    bool ValidatorsContainer::validate(const Messages::Message &msg) const {
        if (!validators.has_key(msg.command_name)) {
            return false;
        }
        for (const auto &validator : validators[msg.command_name]) {
            bool result = validator(msg);
            if (!result) {
                return result;
            }
        }
        return true;
    }

    bool ValidatorsContainer::operator()(const Messages::Message &msg) const {
        return validate(msg);
    }
}