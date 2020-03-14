#include "MessageFormater.h"
using namespace std;

ParameterIterator::ParameterIterator(const String& parameters):
    _parameters(parameters), current_parameter(""), current_position(0)
{
    ++(*this); // инкремент реализует получение следующего параметра, т.е. здесь будет получен первый параметр
}

ParameterIterator::ParameterIterator(const ParameterIterator& iterator):
    _parameters(iterator._parameters), 
    current_parameter(iterator.current_parameter), current_position(iterator.current_position)
{
}

bool ParameterIterator::HasValue(){

    return current_parameter != HAS_NO_VALUE;
}

String ParameterIterator::GetValue(){

    if (current_parameter == HAS_NO_VALUE){

        return "";
    }
    else{

        return current_parameter;
    }
    
}

ParameterIterator& ParameterIterator::operator++(){

    if (current_position >= _parameters.length()){

        current_parameter = HAS_NO_VALUE;
    }
    else{

        int end = current_position;

        while (_parameters[end] != MessageFormater::symbol_parameters_splitter){

            ++end;
            if (end == _parameters.length()){

                break;
            }
        }

        current_parameter = _parameters.substring(current_position, end);
        current_position = end + 1;
    }

    return *this;
}

ParameterIterator ParameterIterator::operator++(int){

    ParameterIterator temp(*this);

    ++(*this);

    return temp;
}

bool ParameterIterator::operator==(const ParameterIterator& compared_iterator){

    return this->current_parameter == compared_iterator.current_parameter;
}

MessageFormater::MessageFormater(){
    
    this->receiver = "";
    this->theme = "";
    this->parameters = "";
}

MessageFormater::MessageFormater(String receiver_, String theme_){
    
    this->receiver = receiver_;
    this->theme = theme_;

    this->parameters = "";
}

String MessageFormater::Receiver(){

    return receiver;
}

String MessageFormater::Theme(){

    return theme;
}

bool MessageFormater::AddParameter(const String& parameter_){

    bool result;

    const String& par = parameter_;
    if (ContainsSpecialSymbols(par)){

        result = false;
    }
    else{

        result = true;
        if (parameters.equals("")){

            parameters += parameter_;
        }
        else{

            parameters += symbol_parameters_splitter;
            parameters += parameter_;
        }
        
    }
    
    return result;
}

String MessageFormater::GetMessage(){

    String message = "";

    if (MessageIsCorrect()){

        message += symbol_message_starter_ender;

        AddHeader(message);
        AddParameters(message);

        message += symbol_message_starter_ender;
    }

    return message;
}

String MessageFormater::TryParseMessage(const String& message){

    String error_messages = "";
    String header;
    String params;

    if (message.equals(""))
    {
        error_messages += "Empty message. ";
    }
    else 
    {
        int pos = 0;
        const String& mes = message;

        Accept(mes, pos, symbol_message_starter_ender, error_messages);
        header = ParseHeader(mes, pos, error_messages);
        params = ParseParameters(mes, pos, error_messages);

        Accept(mes, pos, symbol_message_starter_ender, error_messages);
    }

    if (error_messages == "")
    {
        receiver = header.substring(0, header.indexOf(symbol_parameters_splitter));
        theme = header.substring(header.indexOf(symbol_parameters_splitter) + 1);
        parameters = params;
    }

    return error_messages;
}

ParameterIterator MessageFormater::GetParametersIterator(){

    if (MessageIsCorrect()) 
    {
        return ParameterIterator(this->parameters);
    } 
    else
    {
        return ParameterIterator(""); 
    }
    
}

bool MessageFormater::ContainsSpecialSymbols(const String& s){

    bool result = false;
    for (int i = 0; i < s.length(); i++)
    {
        if (IsSpecialSymbol(s[i]))
        {
            result = true;
            break;
        }
    }

    return result;
}

bool MessageFormater::IsSpecialSymbol(char c){

    return (

        c == symbol_message_starter_ender ||
        c == symbol_header_starter ||
        c == symbol_header_ender ||
        c == symbol_parameters_starter ||
        c == symbol_parameters_ender ||
        c == symbol_parameters_splitter
    );
}

bool MessageFormater::MessageIsCorrect()
{
    // if message was parsed correctly, it has to have the receiver and the theme
    return receiver != "" && theme != ""; 
}

void MessageFormater::AddHeader(String& message){

    message += symbol_header_starter;

    message += this->receiver;
    message += symbol_parameters_splitter;
    message += this->theme;

    message += symbol_header_ender;
}

void MessageFormater::AddParameters(String& message){

    message += symbol_parameters_starter;

    message += this->parameters;

    message += symbol_parameters_ender;
}

void MessageFormater::Accept(const String& s, int& position, char expected, String& errors){

    if(s[position] == expected){

        ;
    }
    else if (errors == ""){

        errors = String(position) + " position: found \'" + s[position] + "\', expect \'" + expected + "\'. ";
    }

    if (position < s.length()){

        position++;
    }  
}

String MessageFormater::ParseHeader(const String& s, int& position, String& errors){

    String header("");
    Accept(s, position, symbol_header_starter, errors);
    
    int start_position = position;
    SkipUntil(s, position, symbol_parameters_splitter, errors);
    Accept(s, position, symbol_parameters_splitter, errors);
    SkipUntil(s, position, symbol_header_ender, errors);
    header += s.substring(start_position, position);

    Accept(s, position, symbol_header_ender, errors);

    return header;
}

String MessageFormater::ParseParameters(const String& s, int& position, String& errors){

    String params("");
    Accept(s, position, symbol_parameters_starter, errors);

    int start_position = position;

    while (s[position] != symbol_parameters_ender){

        if (s.substring(position).indexOf(';') != -1){

            SkipUntil(s, position, symbol_parameters_splitter, errors);
            Accept(s, position, symbol_parameters_splitter, errors);
        }
        else{

            SkipUntil(s, position, symbol_parameters_ender, errors);
            break;
        }
    }
    params += s.substring(start_position, position);
    Accept(s, position, symbol_parameters_ender, errors);

    return params;
}

void MessageFormater::SkipUntil(const String& s, int& position, char expecting, String& errors){

    while (s[position] != expecting){

        if (IsSpecialSymbol(s[position]) && errors == ""){

            errors = String(position) + ": unexpected symbol \'" + s[position] + "\', looking for \'" + expecting + "\'";
        }

        if (position < s.length()){

            position++;
        }
        else{   
            
            position--;
            break;
        }
    }
}