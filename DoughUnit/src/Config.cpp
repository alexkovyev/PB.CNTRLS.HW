#include <Config.h>
#include <CurrentPositionsDirections.h>

const int pulses_in_microsec = 16; 
const int steps_in_mm = 25;

int give_motor_delay_between_steps_microsec = 1200;
int lift_motor_delay_between_steps_microsec = 2000;

bool inverse_giving_direction = false;
bool inverse_lifting_direction = false;

int max_recover_step_number = 200;
int additional_lifting_step_number = 50;

long max_give_step_number = 2000;
long max_lift_step_number = 20000;


long StrToLong(String number);

void Setup(ParameterIterator parameters){

    give_motor_delay_between_steps_microsec = StrToLong(parameters.GetValue());
    ++parameters;
    lift_motor_delay_between_steps_microsec = StrToLong(parameters.GetValue());
    ++parameters;

    inverse_giving_direction = StrToLong(parameters.GetValue());
    Serial.print(inverse_giving_direction); //dbg
    ++parameters;
    inverse_lifting_direction = StrToLong(parameters.GetValue());
    Serial.print(inverse_lifting_direction); //dbg
}

long StrToLong(String number){
    
    long result = 0;

    int pos = 0;
    int sign = 1;
    if (number[0] == '-'){
        
        ++pos;
        sign = -1;
    }

    for (; pos < number.length(); ++pos){

        result = result*10 + number[pos] - '0';
    }

    return result * sign;
}