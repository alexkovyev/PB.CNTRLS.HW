/*
    This is an interface between pc and controller
    Incapsulates serial port working
    
    It ignores all unformated data that comes to port,
    Returns only formated message

    Realises some methods that can send formated messages to the port
*/

#pragma once
#include "Arduino.h"
#include "MessageFormater.h"

bool HasMessage();

MessageFormater GetFormatedMessage();

bool SendMessage(MessageFormater messageFormater);

void SendCommandReceivedMessage(const String& command_name);
void SendCommandExecutedMessage(const String& command_name);

void SendIncorrectCommandMessage(const String& command_name, const String& command_errors);
void SendErrorMessage(const String& errors);
