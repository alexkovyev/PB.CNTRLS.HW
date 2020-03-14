/*
    This file contain current controller state
    States allows to know when long procedure ends for sending executed messages
    And for starting procedures that should be run after some other procedure finished

    This can be considered as a call-backs mechanism
*/

#pragma once

enum State{

    waiting,

    prepare_giving,
    prepare_giving_finished,
    giving,
    giving_finished,

    lifting_down,
    lifting_down_finished,

    returning_to_work,
    returning_to_work_finished,

    to_zero,
    to_zero_finished,

    recovering_after_stopper,
    recovering_after_stopper_finished,

    emergency_stop_executed,

    error_stopper_triggered,
    error_cant_recover_after_stopper,
    error_cant_find_stopper,
    error_cant_give_dough,
    error_cant_return_to_work,

    service_moving_give,
    service_moving_give_finished,
    service_moving_lift,
    service_moving_lift_finished
};

extern State state;