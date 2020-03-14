/*
    Common string resources. This file will be included in each unit program
*/

#pragma once
#include <Arduino.h>

extern String sr_pc_name;

extern String sr_error_theme;

extern String sr_command_stop;
extern String sr_command_check_unit_name;
extern String sr_command_get_status;
extern String sr_command_setup;
extern String sr_command_get_coordinates;
extern String sr_command_to_zero;

extern String sr_responce_correct_unit_name;
extern String sr_responce_command_received;
extern String sr_responce_incorrect_command_received;
extern String sr_responce_command_executed;
extern String sr_responce_emergency_stop_executed;

extern String sr_error_stopper_triggered;
extern String sr_error_cant_recover_after_stopper;
extern String sr_error_cant_find_stopper;

extern String sr_command_error_wrong_format;
extern String sr_command_error_unknown_command;
extern String sr_command_error_wrong_unit_name;

bool IsGlobalCommand(String command_name);