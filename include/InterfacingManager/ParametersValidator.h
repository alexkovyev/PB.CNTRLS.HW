//
// Created by prostoichelovek on 16.04.2020.
//

#ifndef ARDU_INTERFACING_MANAGER_PARAMETERSVALIDATOR_H
#define ARDU_INTERFACING_MANAGER_PARAMETERSVALIDATOR_H


#include "InterfacingManager/Message/Message.h"

namespace Interfacing {

    typedef bool(*ValidatorFunction_ptr)(const std::string &);

    class ParametersValidator {
    public:
        ValidatorFunction_ptr fn = nullptr;
        int start_idx = 0, end_idx = 0;

        ParametersValidator() = default;

        ParametersValidator(ValidatorFunction_ptr fn, int startIdx, int endIdx = -1);

        ParametersValidator &operator=(const ParametersValidator &other);

        bool validate(const Messages::Message &msg) const;

        bool operator()(const Messages::Message &msg) const;
    };

}


#endif //ARDU_INTERFACING_MANAGER_PARAMETERSVALIDATOR_H
