#include <Sensors.h>
#include <PinDefine.h>
#include <Arduino.h>

bool StopperTriggered(){

    return !(digitalRead(LIFT_LIMIT_PIN)); // end stoppers are normal close, so need to invert them
}

bool SeeDough(){

    return !(digitalRead(DOUGH_SENSOR)); // sensor is normal close, so need to invert it
}