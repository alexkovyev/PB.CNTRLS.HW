#include <CurrentPositionsDirections.h>
#include <Config.h>
#include <Arduino.h>

long current_position_lifter = 0;

bool current_direction_lifter = 1;
bool current_direction_giver = 1;

void SetLiftDirection(bool direction){

    if (inverse_lifting_direction){

        current_direction_lifter = !direction; 
    }
    else{

        current_direction_lifter = direction;
    }

    digitalWrite(LIFT_DIR_PIN, current_direction_lifter);
}

void SetGiveDirection(bool direction){

    if (inverse_giving_direction){

        current_direction_giver = !direction; 
    }
    else{

        current_direction_giver = direction;
    }

    digitalWrite(GIVE_DIR_PIN, current_direction_giver);
}