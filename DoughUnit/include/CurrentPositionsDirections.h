/*
    This file contains positions, directions and functions for changing directions
*/

#pragma once

extern long current_position_lifter;

extern bool current_direction_lifter;
extern bool current_direction_giver;

void SetLiftDirection(bool direction);

void SetGiveDirection(bool direction);