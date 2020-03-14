/*
    Pin number constants
    Function that sets pins up (changes modes, pull-ups/pull-downs, sets power etc)
*/

#pragma once

#define LIFT_STEP_PIN 4
#define LIFT_DIR_PIN 7
#define LIFT_ENABLE_PIN 13
#define LIFT_LIMIT_PIN 11

#define GIVE_STEP_PIN 3
#define GIVE_DIR_PIN 6

#define DOUGH_SENSOR 10

#define ENABLE_PIN 8

void PinSetup();
