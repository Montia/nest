// timer.cc 
//	Routines to emulate a hardware timer device.
//
//      A hardware timer generates a CPU interrupt every X milliseconds.
//      This means it can be used for implementing time-slicing.
//
//      We emulate a hardware timer by scheduling an interrupt to occur
//      every time stats->totalTicks has increased by TimerTicks.
//
//      In order to introduce some randomness into time-slicing, if "doRandom"
//      is set, then the interrupt is comes after a random number of ticks.
//
//	Remember -- nothing in here is part of Nachos.  It is just
//	an emulation for the hardware that Nachos is running on top of.
//
//  DO NOT CHANGE -- part of the machine emulation
//
// Copyright (c) 1992-1993 The Regents of the University of California.
// All rights reserved.  See copyright.h for copyright notice and limitation 
// of liability and disclaimer of warranty provisions.

#include "copyright.h"
#include "timer.h"
#include "system.h"

// dummy function because C++ does not allow pointers to member functions
static void TimerHandler(int arg)
{ Timer *p = (Timer *)arg; p->TimerExpired(); }

//----------------------------------------------------------------------
// Timer::Timer
//      Initialize a hardware timer device.  Save the place to call
//	on each interrupt, and then arrange for the timer to start
//	generating interrupts.
//
//      "timerHandler" is the interrupt handler for the timer device.
//		It is called with interrupts disabled every time the
//		the timer expires.
//      "callArg" is the parameter to be passed to the interrupt handler.
//      "doRandom" -- if true, arrange for the interrupts to occur
//		at random, instead of fixed, intervals.
//----------------------------------------------------------------------

Timer::Timer(VoidFunctionPtr timerHandler, int callArg, bool doRandom)
{
    randomize = doRandom;
    handler = timerHandler;
    arg = callArg; 

    // DO NOT CHANGE DEBUG MESSAGES
    DEBUG('n', "Timer's interval is set to %d%s\n", TimerTicks, doRandom?" randomly":"");

    // schedule the first interrupt from the timer device
    interrupt->Schedule(TimerHandler, (int) this, TimeOfNextInterrupt(), 
		TimerInt); 
}

//----------------------------------------------------------------------
// Timer::TimerExpired
//      Routine to simulate the interrupt generated by the hardware 
//	timer device.  Schedule the next interrupt, and invoke the
//	interrupt handler.
//----------------------------------------------------------------------
void 
Timer::TimerExpired() 
{
    // schedule the next timer device interrupt
    interrupt->Schedule(TimerHandler, (int) this, TimeOfNextInterrupt(), 
		TimerInt);

    // invoke the Nachos interrupt handler for this device
    (*handler)(arg);
}

//----------------------------------------------------------------------
// Timer::TimeOfNextInterrupt
//      Return when the hardware timer device will next cause an interrupt.
//	If randomize is turned on, make it a (pseudo-)random delay.
//----------------------------------------------------------------------

int 
Timer::TimeOfNextInterrupt() 
{
    if (randomize)
	return 1 + (Random() % (TimerTicks * 2));
    else
	return TimerTicks; 
}
