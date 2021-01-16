#include <cstring>
#include "system.h"
#include "synch.h"

#ifndef THREAD_NUM
#define THREAD_NUM 3
#endif

void work(int ticks) {
    ASSERT(interrupt->getLevel() == IntOn);
    for (int i = 0; i < ticks/10; i++) {
        interrupt->SetLevel(IntOff);
        interrupt->SetLevel(IntOn);
    }
}

void postPhase(Barrier& b)
{
    DEBUG('e', "postPhaseAction is called in phase %d\n", b.CurrentPhaseNumber());
}

Barrier barrier(THREAD_NUM, postPhase);

void run(void *p)
{
    int arg = (int)p;
    int workload = arg * 100;
    DEBUG('e', "%s begins\n", currentThread->getName());
    for (int phase = 0; phase < 3; phase++)
    {
        DEBUG('e', "%s starts working for phase %d\n", currentThread->getName(), phase);
        work(workload);
        DEBUG('e', "%s ends working for phase %d\n", currentThread->getName(), phase);
        barrier.SignalAndWait();
    }
}

int Nest(void *arg) {
    DEBUG('e', "Entering Nest()\n");
    char* threadNames[THREAD_NUM+1];
    threadNames[0] = "main";

    for (int i = 1; i <= THREAD_NUM; i++) 
    {
        threadNames[i] = new char[10];
        sprintf(threadNames[i], "thread%d", i);
        Thread *t = new Thread(threadNames[i]);
        t->Fork(run, (void*)i);
    }

    currentThread->Yield();

    return 0;
}