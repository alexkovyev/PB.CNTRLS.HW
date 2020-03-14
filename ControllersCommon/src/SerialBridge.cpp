#include "SerialBridge.h"
#include <GlobalStringResources.h>
// forward declarations
void FillBufferFromSerial();
bool FindMessageStartEndPositions();
bool ParseMessageAndPrintErrors();
void ExtractMessageFromBuffer();
void CheckMessageForErrors();
// forward declarations

String buffer;
String message;
MESSAGEFORMATER messageFormater = NULL;

int message_begin_position;
int message_end_position;

bool HasMessage(){
    
    bool has_message = false;

    if (messageFormater == NULL){

        messageFormater = new MessageFormater();
        FillBufferFromSerial();

        if (buffer != ""){
            
            if (FindMessageStartEndPositions()){

                has_message = ParseMessageAndPrintErrors();
            }
            else
            {
                Serial.print(buffer); // dbg
                buffer = "";
            }
        }

        if (!has_message){

            delete messageFormater;
            messageFormater = NULL;
        }
    }
    else{

        has_message = true;
    }
    
    return has_message;
}

MessageFormater GetFormatedMessage(){

    MessageFormater formatedMessage = *messageFormater;
    
    delete messageFormater;
    messageFormater = NULL;

    return formatedMessage;
}

bool SendMessage(MessageFormater messageFormater){

    bool sent = false;

    String message(messageFormater.GetMessage());
    if (message != ""){
        
        Serial.print(message);
        sent = true;
    }

    return sent;
}

void SendCommandReceivedMessage(const String& command_name){

    MessageFormater _mes = MessageFormater(sr_pc_name, command_name);
    _mes.AddParameter(sr_responce_command_received);
    SendMessage(_mes);
}

void SendCommandExecutedMessage(const String& command_name){

    MessageFormater _mes = MessageFormater(sr_pc_name, command_name);
    _mes.AddParameter(sr_responce_command_executed);
    SendMessage(_mes);
}

void SendIncorrectCommandMessage(const String& command_name, const String& command_errors){

    MessageFormater _mes(sr_pc_name, sr_responce_incorrect_command_received);
    _mes.AddParameter(command_errors);
    SendMessage(_mes);
}

void SendErrorMessage(const String& errors){

    MessageFormater _mes(sr_pc_name, sr_error_theme);
    _mes.AddParameter(errors);
    SendMessage(_mes);
}

void FillBufferFromSerial(){

    if (Serial.available()){

        buffer += Serial.readString();
    }
}

bool FindMessageStartEndPositions(){

    bool found_message;

    int message_starter_ender_count = 0;

    message_begin_position = message_end_position = 0;

    int pos = 0;
    for (; pos < buffer.length(); ++pos)
    {
        if (buffer[pos] == MessageFormater::symbol_message_starter_ender)
        {
            if (message_starter_ender_count == 0)
            {
                message_begin_position = pos;
                ++message_starter_ender_count;
            }
            else
            {
                message_end_position = pos;
                ++message_starter_ender_count;
                break;
            }
        }
    }

    if (message_starter_ender_count < 2)
    {
        message_begin_position = 0;
        message_end_position = 0;

        found_message = false;
    }
    else
    {
        found_message = true;
    }

    return found_message;
}

bool ParseMessageAndPrintErrors(){

    bool correct_message = false;

    String buffer_copy = buffer;

    ExtractMessageFromBuffer();

    if (messageFormater->TryParseMessage(message) == ""){

        correct_message = true;
    }
    else{

        Serial.println("\n" + sr_command_error_wrong_format + ". Received: " + buffer_copy + ". Errors: " + messageFormater->TryParseMessage(message));
    }

    return correct_message;
}

void ExtractMessageFromBuffer(){
    
    message = buffer.substring(message_begin_position, message_end_position + 1);
    buffer = buffer.substring(message_end_position + 1);
}