#include <CommandAnalysis.h>
#include <ParametersCheck.h>
#include <GlobalStringResources.h>
#include <LocalStringResources.h>

// forward declarations
String SetupCommandErrors(ParameterIterator parameterIterator);
bool IsRegularCommand(String command_name);
bool IsServiceCommand(String command_name);
String MoveCommandsErrors(ParameterIterator parameters);
bool CheckUnitName();
String ParametersError(ParameterIterator, String(*[])(const String&), int);
// forward declarations

String CommandErrors(MessageFormater message){

    String errors = "";
    if (message.Receiver() != sr_unit_name){

        errors = sr_command_error_wrong_unit_name;
    }
    else{
        
        String command_name = message.Theme();
        
        if (command_name == sr_command_setup){

            errors += SetupCommandErrors(message.GetParametersIterator());
        }
        else if (IsGlobalCommand(command_name)){

            // this commands don't contain parameters, no need for additional checks
        }
        else if (IsRegularCommand(command_name)){

            // this commands don't contain parameters, no need for additional checks
        }
        else if (IsServiceCommand(command_name)){

            errors += MoveCommandsErrors(message.GetParametersIterator());
        }
        else if (command_name == sr_command_get_coordinates){

            // this commands don't contain parameters, no need for additional checks
        }
        else{

            errors += sr_command_error_unknown_command;
        }
    }
    
    return errors;
}

String SetupCommandErrors(ParameterIterator parameters){
    
    String errors = "";

    String (*checks[4])(const String&) = {
        
        IsPositive,
        IsPositive,
        IsBoolean,
        IsBoolean
    };

    errors += ParametersErrors(parameters, checks, sizeof(checks) / sizeof(checks[0]));

    return errors; 
}

bool IsRegularCommand(String command_name){

    return (

        command_name == sr_command_give || 
        command_name == sr_command_lift_down || 
        command_name == sr_command_return_to_work
    );
}

bool IsServiceCommand(String command_name){

    return (

        command_name.equals(sr_service_command_move_lift) || 
        command_name.equals(sr_service_command_move_give)
    );
}

String MoveCommandsErrors(ParameterIterator parameters){

    String errors = "";

    String (*checks[1])(const String&) = {
        
        IsNumber
    };

    errors += ParametersErrors(parameters, checks, 1);

    return errors;
}


