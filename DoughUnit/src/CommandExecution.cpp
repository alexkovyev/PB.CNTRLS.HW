#include <CommandExecution.h>
#include <CommandAnalysis.h>
#include <GlobalStringResources.h>
#include <LocalStringResources.h>
#include <State.h>
#include <SerialBridge.h>
#include <Config.h>
#include <Mover.h>
#include <CurrentPositionsDirections.h>

// forward declarations
void ExecuteGlobalCommand(MessageFormater message);
void ExecuteRegularCommand(String command_name);
void ExecuteMoveCommand(MessageFormater message);
void EmergencyStop();
void SendStatus();
void SendCoordinates();
void SendNameConfirm();
// forward declarations

void ExecuteCommand(MessageFormater message){

    String command_name = message.Theme();

    if (IsGlobalCommand(command_name)){

        ExecuteGlobalCommand(message);
    }
    // move commands can only be executed if controller is free
    else if (state == waiting){

        if (IsRegularCommand(command_name)){

            ExecuteRegularCommand(command_name);
        }
        else if (IsServiceCommand(command_name)){

            ExecuteMoveCommand(message);
        }
    }
}

void ExecuteGlobalCommand(MessageFormater message){

    String command_name = message.Theme();

    if (command_name.equals(sr_command_stop)){

        EmergencyStop();
    }
    else if (command_name.equals(sr_command_check_unit_name)){

        SendNameConfirm();
    }
    else if (command_name.equals(sr_command_get_status)){

        SendStatus();
    }
    else if (command_name.equals(sr_command_setup)){

        Setup(message.GetParametersIterator());
    }
    else if (command_name.equals(sr_command_get_coordinates)){

        SendCoordinates();
    }
    else if (command_name.equals(sr_command_to_zero)){

        SendCommandReceivedMessage(command_name);
        state = to_zero;
        InitiateToZero();
    }
}

void ExecuteRegularCommand(String command_name){

    if (command_name.equals(sr_command_give)){

        SendCommandReceivedMessage(command_name);
        state = prepare_giving;
        InitiateToTop();
    }
    else if (command_name.equals(sr_command_lift_down)){

        SendCommandReceivedMessage(command_name);
        state = lifting_down;
        InitiateToZero();
    }
    else if (command_name.equals(sr_command_return_to_work)){

        SendCommandReceivedMessage(command_name);
        state = returning_to_work;
        InitiateToTop();
    }
}

void ExecuteMoveCommand(MessageFormater message){

    String command_name = message.Theme();

    if (command_name.equals(sr_service_command_move_give)){

        SendCommandReceivedMessage(command_name);
        state = service_moving_give;
        Service_InitiateMove(GIVE_STEP_PIN, StrToLong(message.GetParametersIterator().GetValue()));
    }
    else if (command_name.equals(sr_service_command_move_lift)){

        SendCommandReceivedMessage(command_name);
        state = service_moving_lift;
        Service_InitiateMove(LIFT_STEP_PIN, StrToLong(message.GetParametersIterator().GetValue()));
    }
}

void EmergencyStop(){
    
    if (state != waiting){

        AbortMove();
    }
}

void SendStatus(){

    MessageFormater message("PC", sr_command_get_status);
    message.AddParameter(String(state));

    SendMessage(message);
}

void SendCoordinates(){

    MessageFormater message(sr_pc_name, sr_command_get_coordinates);
    message.AddParameter(String(current_position_lifter));

    SendMessage(message);
}

void SendNameConfirm(){

    MessageFormater message(sr_pc_name, sr_command_check_unit_name);
    message.AddParameter(sr_responce_correct_unit_name);
    SendMessage(message);
}