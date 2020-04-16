//
// Created by prostoichelovek on 16.04.2020.
//

#ifndef ARDU_INTERFACING_MANAGER_MYMAP_HPP
#define ARDU_INTERFACING_MANAGER_MYMAP_HPP


#include "map"

#include "utils.hpp"

namespace Interfacing {

    template<typename Key_T, typename Val_T>
    class MyMap {
    public:
        MyMap() = default;

        bool has_key(const Key_T &key) const {
            return std::find(keys.begin(), keys.end(), key) != keys.end();
        }

        Val_T &operator[](const Key_T &key) {
            if (!has_key(key)) {
                keys.push_back(key);
                values.push_back(Val_T());
                return values.back();
            }
            const auto key_it = std::find(keys.begin(), keys.end(), key);
            const unsigned int key_idx = std::distance(keys.begin(), key_it);
            return values[key_idx];
        }

    private:
        std::vector<Key_T> keys;
        std::vector<Val_T> values;

    };

}

#endif //ARDU_INTERFACING_MANAGER_MYMAP_HPP
