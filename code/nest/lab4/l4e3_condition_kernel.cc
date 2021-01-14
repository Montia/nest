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
Condition condition("l4e3_condition");

void run(void *p)
{
    DEBUG('e', "%s begins\n", currentThread->getName());
    lock.Acquire();
    DEBUG('e', "%s acquired lock\n", currentThread->getName());
    DEBUG('e', "%s starts waiting\n", currentThread->getName());
    condition.Wait(&lock);
    DEBUG('e', "%s finished waiting\n", currentThread->getName());
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

    work(500);
    lock.Acquire();
    DEBUG('e', "%s signaling one thread\n", currentThread->getName());
    condition.Signal(&lock);
    DEBUG('e', "%s signaled one thread\n", currentThread->getName());
    lock.Release();
    work(500);
    lock.Acquire();
    DEBUG('e', "%s broadcasting all threads\n", currentThread->getName());
    condition.Broadcast(&lock);
    DEBUG('e', "%s broadcasted all threads\n", currentThread->getName());
    lock.Release();

    return 0;
}