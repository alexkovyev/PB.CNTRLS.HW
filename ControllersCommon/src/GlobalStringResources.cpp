#include <GlobalStringResources.h>

String sr_pc_name = "Pc";

String sr_error_theme = "Error";

String sr_command_stop = "Stop";
String sr_command_check_unit_name = "It's you?";
String sr_command_get_status = "Status";
String sr_command_setup = "Setup";
String sr_command_get_coordinates = "Get coordinates";
String sr_command_to_zero = "To zero";

String sr_responce_correct_unit_name = "It's me";
String sr_responce_command_received = "Received";
String sr_responce_incorrect_command_received = "Incorrect command";
String sr_responce_command_executed = "Executed";
String sr_responce_emergency_stop_executed = "Emergency stop has been executed";

String sr_error_stopper_triggered = "Stopper triggered";
String sr_error_cant_recover_after_stopper = "Cant recover after stopper";
String sr_error_cant_find_stopper = "Cant find stopper";

String sr_command_error_wrong_format = "Wrong format";
String sr_command_error_unknown_command = "Unknown command";
String sr_command_error_wrong_unit_name = "Wrong unit name";

bool IsGlobalCommand(String command_name){

    return (

        command_name.equals(sr_command_check_unit_name) ||
        command_name.equals(sr_command_stop) ||
        command_name.equals(sr_command_get_status) ||
        command_name.equals(sr_command_setup) ||
        command_name.equals(sr_command_get_coordinates) ||
        command_name.equals(sr_command_to_zero) 
    );
}