/*
    Checking commands for errorrs
    Defining if its regulaar or service command
*/

#pragma once
#include <Arduino.h>
#include <MessageFormater.h>

#define UNIT_NAME "Dough"
#define SETUP_COMMAND_NAME "setup"
#define GIVE_COMMAND_NAME "give"
#define LIFT_DOWN_COMMAND_NAME "lift down"
#define BACK_TO_WORK_COMMAND_NAME "to work"

String CommandErrors(MessageFormater message);

bool IsRegularCommand(String command_name);
bool IsServiceCommand(String command_name);

String IsPositive(const String& s);
String IsNumber(const String& s);
String IsDigit(char symbol);
String IsBoolean(const String& s);
