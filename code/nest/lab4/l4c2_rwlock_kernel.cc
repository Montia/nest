#include <cstring>
#include "system.h"
#include "synch.h"

#ifndef THREAD_NUM
#define THREAD_NUM 10
#endif

void work(int ticks) {
    ASSERT(interrupt->getLevel() == IntOn);
    for (int i = 0; i < ticks/10; i++) {
        interrupt->SetLevel(IntOff);
        interrupt->SetLevel(IntOn);
    }
}

ReaderWriterLock rwlock;

void reader(void *p)
{
    // int arg = (int)p;
    // int workload = arg * 100;
    DEBUG('e', "%s begins\n", currentThread->getName());
    rwlock.AcquireReaderLock();
    DEBUG('e', "%s acquired reader lock\n", currentThread->getName());
    work(500);
    DEBUG('e', "%s released reader lock\n", currentThread->getName());
    rwlock.ReleaseReaderLock();
}

void writer(void *p)
{
    // int arg = (int)p;
    // int workload = arg * 100;
    DEBUG('e', "%s begins\n", currentThread->getName());
    rwlock.AcquireWriterLock();
    DEBUG('e', "%s acquired writer lock\n", currentThread->getName());
    work(500);
    DEBUG('e', "%s released writer lock\n", currentThread->getName());
    rwlock.ReleaseWriterLock();
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
        if (i % 5 == 0)
        {
            t->Fork(writer, (void*)i);
        }
        else
        {
            t->Fork(reader, (void*)i);
        }
        currentThread->Yield();
    }
    return 0;
}