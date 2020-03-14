#include "Arduino.h"
#include <PinDefine.h>
#include <Mover.h>
#include <CommandAnalysis.h>
#include <Config.h>
#include <MessageFormater.h>
#include <SerialBridge.h>
#include <GlobalStringResources.h>
#include <LocalStringResources.h>
#include <State.h>
#include <CommandExecution.h>
#include <Sensors.h>

// forward declarations
void CheckMessage();
void CheckState();
void CheckCommandFinishedState();
void CheckErrorState();
// forward declarations

MessageFormater mes;


void setup() {

    Serial.begin(115200);
    PinSetup();
}

void loop(){

    CheckMessage();
    CheckState();
}

void CheckMessage(){
    
    if (HasMessage()){
        
        mes = GetFormatedMessage();
        String command_errors = CommandErrors(mes);
        if (command_errors.equals("")){
            
            ExecuteCommand(mes);
        }
        else{

            SendIncorrectCommandMessage(mes.Theme(), command_errors);
        }
    }
}

void CheckState(){

    if (state == emergency_stop_executed){

        mes = MessageFormater(sr_pc_name, sr_responce_emergency_stop_executed);
        SendMessage(mes);
        state = waiting;
    }
    else{

        CheckCommandFinishedState();
        CheckErrorState();
    }
}

void CheckCommandFinishedState(){

    switch(state){

        case to_zero_finished:
            SendCommandExecutedMessage(sr_command_to_zero);
            state = waiting;
            break;

        case prepare_giving_finished:
            state = giving;
            InitiateGiving();
            break;

        case giving_finished:
            SendCommandExecutedMessage(sr_command_give);
            state = waiting;
            break;
        
        case lifting_down_finished:
            SendCommandExecutedMessage(sr_command_lift_down);
            state = waiting;
            break;
        
        case returning_to_work_finished:
            SendCommandExecutedMessage(sr_command_return_to_work);
            state = waiting;
            break;
        
        case recovering_after_stopper_finished:
            state = waiting;
            break;

        case service_moving_give_finished:
            SendCommandExecutedMessage(sr_service_command_move_give);
            state = waiting;
            break;

        case service_moving_lift_finished:
            SendCommandExecutedMessage(sr_service_command_move_lift);
            state = waiting;
            break;
    }
}

void CheckErrorState(){

    switch (state){
        case error_stopper_triggered:
            SendErrorMessage(sr_error_stopper_triggered);
            state = waiting;
            break;

        case error_cant_recover_after_stopper:
            SendErrorMessage(sr_error_cant_recover_after_stopper);
            state = waiting;
            break;
        
        case error_cant_find_stopper:
            SendErrorMessage(sr_error_cant_find_stopper);
            state = waiting;
            break;
        
        case error_cant_give_dough:            
            SendErrorMessage(sr_error_cant_give_dough);
            state = waiting;
            break;
                
        case error_cant_return_to_work:
            SendErrorMessage(sr_error_cant_return_to_work);
            state = waiting;
            break;
    }
}