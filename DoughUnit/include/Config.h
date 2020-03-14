/*
    This module contains project setups and config function

    Parameters that can be set with config function are in configurable section
*/

#pragma once
#include <Arduino.h>
#include <CommandAnalysis.h>
#include <PinDefine.h>

extern const int pulses_in_microsec; 
extern const int steps_in_mm;

// configurable parameters
extern int give_motor_delay_between_steps_microsec;
extern int lift_motor_delay_between_steps_microsec;

extern bool inverse_giving_direction;// don't know how the motor will be installed in unit
                                     // this params allow to change directions of each motor to an opposite
                                     // (e.g. when trying to lift platform up, it goes down => inverse lifting direction)
extern bool inverse_lifting_direction;
// configurable parameters


extern int max_recover_step_number;
extern int additional_lifting_step_number;

extern long max_give_step_number;
extern long max_lift_step_number;

void Setup(ParameterIterator parameters);

long StrToLong(String number);
