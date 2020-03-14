#include <Mover.h>
#include <State.h>
#include <PinDefine.h>
#include <Config.h>
#include <CurrentPositionsDirections.h>
#include <Sensors.h>

// forward declarations
void _AbortMove(State after_abort_state);

void StartTimer(int delay_between_steps_in_micsec);
void StopTimer();

void GivingMover();
void ToZeroMover();
void DoughToTopMover();
void StepMover();

bool DoughToTop_CanMove();

void DoStep(int step_pin);
void HandleStopper();

bool RecoverAfterStopper();
void AdditionalLifting();

void ChangeState();

void ChangeLiftPosition();
// forward declarations

long steps_made; // move will be aborted if there was more steps than max_step_number (for giving, lifting, returning and after stopper recovering)

int step_pin;
long _steps_number;

bool abort_move;

enum MoveMode{

    mode_giving,
    mode_to_zero,
    mode_to_top,
    mode_step_number
} move_mode;

void InitiateGiving(){

    move_mode = mode_giving;
    steps_made = 0;

    SetGiveDirection(HIGH);

    StartTimer(give_motor_delay_between_steps_microsec);
}

void InitiateToZero(){

    move_mode = mode_to_zero;
    steps_made = 0;

    SetLiftDirection(LOW);

    StartTimer(lift_motor_delay_between_steps_microsec);
}

void InitiateToTop(){

    move_mode = mode_to_top;
    steps_made = 0;

    SetLiftDirection(HIGH);

    StartTimer(lift_motor_delay_between_steps_microsec);
}

void Service_InitiateMove(int pin, long step_number){

    step_pin = pin;
    _steps_number = abs(step_number);
    move_mode = mode_step_number;
    steps_made = 0;

    if (step_pin == GIVE_STEP_PIN){

        SetGiveDirection(step_number > 0);
        StartTimer(give_motor_delay_between_steps_microsec);
    }
    else{

        SetLiftDirection(step_number > 0);
        StartTimer(lift_motor_delay_between_steps_microsec);
    }

}

void AbortMove(){

    abort_move = true;
}

void _AbortMove(State after_abort_state){
    
    StopTimer();

    state = after_abort_state;
    abort_move = false;
}

void StartTimer(int delay_between_steps_in_micsec){

    cli();  // отключить глобальные прерывания
    TCCR1A = 0; // сброс регистров
    TCCR1B = 0;

    // установить регистр совпадения. Прерывание будет вызвано после этого числа тактов
    // в микросекунде 16 тиков таймера, делителя частоты 16 нет
    // выбран делитель 64, число микросекунд делится на 4
    OCR1A = delay_between_steps_in_micsec / 4;

    TCCR1B |= (1 << WGM12);  // включить таймер в режим CTC
    TCCR1B |= (1 << CS11);
    TCCR1B |= (1 << CS10);  // делитель частоты 64

    TIMSK1 |= (1 << OCIE1A);  // включить прерывание по совпадению таймера 

    sei();  // включить глобальные прерывания
}

void StopTimer(){

    cli(); 
    TCCR1B = 0;
    sei();
}

void ChangeState(){

    switch(state){

        case to_zero:
            state = to_zero_finished;
            break;

        case prepare_giving:
            state = prepare_giving_finished;
            break;

        case giving:
            state = giving_finished;
            break;
        
        case lifting_down:
            state = lifting_down_finished;
            break;

        case returning_to_work:
            state = returning_to_work_finished;
            break;

        case service_moving_give:
            state = service_moving_give_finished;
            break;

        case service_moving_lift:
            state = service_moving_lift_finished;
            break;
    }
}

// timer interrupt handler
ISR(TIMER1_COMPA_vect){

    switch(move_mode){

        case mode_giving:
            GivingMover();
            break;

        case mode_to_zero:
            ToZeroMover();
            break;

        case mode_to_top:
            DoughToTopMover();
            break;

        case mode_step_number:
            StepMover();
            break;
    }
}

void GivingMover(){

    bool see_dough = SeeDough(); // giving will finish after I stop seeing dough

    if (abort_move){

        _AbortMove(emergency_stop_executed);
    }
    else if (see_dough){

        if (steps_made < max_give_step_number){

            digitalWrite(GIVE_STEP_PIN, HIGH);
            digitalWrite(GIVE_STEP_PIN, LOW);
            ++steps_made;
        }
        else{

            _AbortMove(error_cant_give_dough);
        }
    }
    else{

        StopTimer();
        ChangeState();
    }
}

void ToZeroMover(){

    bool stopper_not_triggered = !StopperTriggered();

    if (abort_move){

        _AbortMove(emergency_stop_executed);
    }
    else{

        if (stopper_not_triggered){

            if (steps_made < max_lift_step_number){

                DoStep(LIFT_STEP_PIN);
                ChangeLiftPosition();
                ++steps_made;
            }
            else{

                _AbortMove(error_cant_find_stopper);
            }
        }
        else{
            StopTimer();
            if (RecoverAfterStopper()){
                
                current_position_lifter = 0;
                ChangeState();
            }
            else{

                _AbortMove(error_cant_recover_after_stopper);
            }
        }
    }
}

void DoughToTopMover(){

    bool dont_see_dough = !SeeDough(); // lift platform until I see dough
    
    if (DoughToTop_CanMove()){

        if (dont_see_dough){

            if (steps_made < max_lift_step_number){

                DoStep(LIFT_STEP_PIN);
                ChangeLiftPosition();
                ++steps_made;
            }
            else{
                
                _AbortMove(error_cant_return_to_work);
            }
            
        }
        else{

            StopTimer();
            AdditionalLifting();
            ChangeState();
        }
    }
}

void StepMover(){

    if (abort_move){

        _AbortMove(emergency_stop_executed);
    }
    else if (StopperTriggered()){

        HandleStopper();
    }
    else if (steps_made < _steps_number){

        DoStep(step_pin);
        if (step_pin == LIFT_STEP_PIN){

            ChangeLiftPosition();
        }
        ++steps_made;
    }
    else{

        StopTimer();
        ChangeState();
    }
}

bool DoughToTop_CanMove(){

    bool can_move = true;
    bool stopper = StopperTriggered();

    if (abort_move){

        _AbortMove(emergency_stop_executed);
        can_move = false;
    }
    else if (stopper){

        HandleStopper();
        
        can_move = false;
    }

    return can_move;
}

void HandleStopper(){

    StopTimer();
    if (RecoverAfterStopper()){

        _AbortMove(error_stopper_triggered);
    }
    else{

        _AbortMove(error_cant_recover_after_stopper);
    }
}

bool RecoverAfterStopper(){

    bool recovered = false;

    steps_made = 0;

    current_direction_lifter = !current_direction_lifter; // need to move out from stopper, so changing direction to opposite
    digitalWrite(LIFT_DIR_PIN, current_direction_lifter);

    while (StopperTriggered() && steps_made < max_recover_step_number){

        DoStep(LIFT_STEP_PIN);
        ChangeLiftPosition();
        ++steps_made;
        delayMicroseconds(lift_motor_delay_between_steps_microsec);
    }

    if (!StopperTriggered()){

        recovered = true;
    }

    return recovered;
}

// dough sensor most likely will be a bit lower than dough should be before giving
// therefore need an extra lifting after sensor triggered
void AdditionalLifting(){

    for (int i = 0; i < additional_lifting_step_number; ++i){

        DoStep(LIFT_STEP_PIN);
        ChangeLiftPosition();
        delayMicroseconds(lift_motor_delay_between_steps_microsec);

        if (StopperTriggered()){

            break;
        }
    }

    if (StopperTriggered()){

        HandleStopper();
    }
}

void DoStep(int step_pin){

    digitalWrite(step_pin, HIGH);
    digitalWrite(step_pin, LOW);
}

void ChangeLiftPosition(){

    if (current_direction_lifter){

        ++current_position_lifter;
    }
    else{

        --current_position_lifter;
    }
}