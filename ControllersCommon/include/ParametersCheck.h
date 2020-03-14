/*
    Function, that checks parameters via iterator, and common check functions
*/

#pragma once
#include <Arduino.h>
#include <MessageFormater.h>

// applying corresponding check function from function array "checks" for each parameter from parameter iterator
// check function should return error_message, or "" if parameter is correct
String ParametersErrors(ParameterIterator iterator, String(*checks[])(const String&), int parameters_number);

// standart check funtions
String IsNumber(const String& s);
String IsPositive(const String& s);
String IsDigit(char symbol);
String IsBoolean(const String& s);
