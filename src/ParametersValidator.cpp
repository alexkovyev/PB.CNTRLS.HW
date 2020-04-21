//
// Created by prostoichelovek on 16.04.2020.
//

#include "InterfacingManager/ParametersValidator.h"

namespace Interfacing {

    ParametersValidator::ParametersValidator(ValidatorFunction_ptr fn, int startIdx, int endIdx)
            : fn(fn), start_idx(startIdx), end_idx(endIdx) {
        if (end_idx == -1) {
            end_idx = start_idx + 1;
        }
    }

    ParametersValidator &ParametersValidator::operator=(const ParametersValidator &other) {
        fn = other.fn;
        start_idx = other.start_idx;
        end_idx = other.end_idx;
        return *this;
    }

    bool ParametersValidator::validate(const Messages::Message &msg) const {
        if (!fn) {
            return true;
        }
        if (msg.parameters.size() < end_idx) {
            return false;
        }
        for (int i = start_idx; i <= end_idx; ++i) {
            bool result = fn(msg.parameters[i]);
            if (!result) {
                return result;
            }
        }
        return true;
    }

    bool ParametersValidator::operator()(const Messages::Message &msg) const {
        return validate(msg);
    }

}