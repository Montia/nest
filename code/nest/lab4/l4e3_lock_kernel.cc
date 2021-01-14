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

Lock lock("l4e3_lock");

void run(void *p)
{
    DEBUG('e', "%s begins\n", currentThread->getName());
    lock.Acquire();
    DEBUG('e', "%s acquired lock\n", currentThread->getName());
    work(1000);
    DEBUG('e', "%s finished work\n", currentThread->getName());
    lock.Release();
    DEBUG('e', "%s released lock\n", currentThread->getName());
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