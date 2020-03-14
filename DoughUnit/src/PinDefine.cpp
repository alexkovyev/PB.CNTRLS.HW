#include <PinDefine.h>
#include "Arduino.h"

void PinSetup(){

    pinMode(GIVE_STEP_PIN, OUTPUT);
    pinMode(GIVE_DIR_PIN, OUTPUT);

    pinMode(LIFT_STEP_PIN, OUTPUT);
    pinMode(LIFT_DIR_PIN, OUTPUT);
    pinMode(LIFT_ENABLE_PIN, OUTPUT);

    pinMode(LIFT_LIMIT_PIN, INPUT);
    digitalWrite(LIFT_LIMIT_PIN, HIGH); // подтяжка концевиков

    pinMode(DOUGH_SENSOR, INPUT);
    
    pinMode(ENABLE_PIN, OUTPUT);
    digitalWrite(8, LOW);
}