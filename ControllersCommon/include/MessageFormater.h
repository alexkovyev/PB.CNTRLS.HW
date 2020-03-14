/*
    This class allows creating and parsing formated messages
    It also can return parameters iterator
*/

#pragma once
#include "Arduino.h"

class ParameterIterator
{
    public:
        ParameterIterator(const String& parameters);
        ParameterIterator(const ParameterIterator& iterator);

        bool HasValue();
        String GetValue();

        ParameterIterator& operator ++();
        ParameterIterator operator ++(int);
        bool operator ==(const ParameterIterator& compared_iterator);

    private:
        const String HAS_NO_VALUE = "#END#";

        const String _parameters;

        String current_parameter;
        int current_position;
};

class MessageFormater
{
    public:
        static const char symbol_message_starter_ender = '#';
        static const char symbol_header_starter = '[';
        static const char symbol_header_ender = ']';
        static const char symbol_parameters_starter = '(';
        static const char symbol_parameters_ender = ')';
        static const char symbol_parameters_splitter = ';';

    public:
        MessageFormater();
        MessageFormater(String receiver_, String theme_);

        String Receiver();
        String Theme();

        bool AddParameter(const String& parameter);

        String GetMessage();
        String TryParseMessage(const String& message);

        ParameterIterator GetParametersIterator();
        
    private:
        String receiver;
        String theme;
        String parameters;
    private:
        bool ContainsSpecialSymbols(const String& s);
        bool IsSpecialSymbol(char c);

        bool MessageIsCorrect();

        void AddHeader(String& message);
        void AddParameters(String& message);

        void Accept(const String& s, int& position, char expected, String& errors);
        String ParseHeader(const String& s, int& position, String& errors);
        String ParseParameters(const String& s, int& position, String& errors);
        void SkipUntil(const String& s, int& position, char expecting, String& errors);
};

typedef MessageFormater* MESSAGEFORMATER;
