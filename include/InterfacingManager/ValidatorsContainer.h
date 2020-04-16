//
// Created by prostoichelovek on 16.04.2020.
//

#ifndef ARDU_INTERFACING_MANAGER_VALIDATORSCONTAINER_H
#define ARDU_INTERFACING_MANAGER_VALIDATORSCONTAINER_H


#include "ParametersValidator.h"
// #include "../.pio/libdeps/uno/ArduinoSTL_ID750/src/map"
#include "MyMap.hpp"

namespace Interfacing {

    class ValidatorsContainer {
    public:
        MyMap<std::string, std::vector<ParametersValidator>> validators;

        ValidatorsContainer() = default;

        void add(const std::string &command, const ParametersValidator &validator);

        void add(const std::string &command, const std::vector<ParametersValidator> &vals);

        bool validate(const Messages::Message &msg) const;

        bool operator()(const Messages::Message &msg) const;
    };

}


#endif //ARDU_INTERFACING_MANAGER_VALIDATORSCONTAINER_H
