/*
    This module contains all moving logic and provides functions to initiate a specific moving.
    Also provides function to abort current move
*/

#pragma once
#include <Arduino.h>
#include <PinDefine.h>


void InitiateGiving();
void InitiateToZero();
void InitiateToTop();

void Service_InitiateMove(int pin, long step_number);

void AbortMove();
