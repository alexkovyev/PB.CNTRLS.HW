#include <ParametersCheck.h>

String ParametersErrors(ParameterIterator iterator, String(*checks[])(const String&), int parameters_number){

    String errors = "";
    for (int i = 0; i < parameters_number; ++i, ++iterator){

        if (!iterator.HasValue()){

            errors += "Not enough parameters: " + String(parameters_number) + " expected, " + String(i+1) + " found. ";
            break;
        }
        else{

            if (checks[i](iterator.GetValue()) != ""){

                errors += String(i+1) + " parameter: " + checks[i](iterator.GetValue());
            }
        }
    }

    if (iterator.HasValue()){

        errors += "Too many parameters: expected " + String(parameters_number) + ". ";
    }

    return errors;
}

String IsNumber(const String& s){

    String error = "";

    int pos = 0;

    if (s[0] == '-'){

        ++pos;
    }

    for (; pos < s.length() - 1; ++pos){

        if (IsDigit(s[pos]) != ""){

            error = "Not a number. ";
            break;
        }
    }

    return error;
}

String IsPositive(const String& s){

    String error = "";
    if (IsNumber(s) == ""){

        if (s[0] == '-'){

            error += "Not a positive number. ";
        }
    } 
    else{

        error += "Not a positive number. ";
    }
    
    return error;
}

String IsDigit(char symbol){

    String error = "";
    if (symbol - '0' < 0 || symbol - '0' > 9)
    {
        error += "Not a digit. ";
    }
    return error;
}

String IsBoolean(const String& s){
    
    String error = "";
    if (s.length() != 1)
    {
        error = "Not a boolean. ";
    }
    else
    {
        if (s[0] != '1' && s[0] != '0')
        {
            error += "Not a boolean. ";
        }
    }
    
    return error;
}