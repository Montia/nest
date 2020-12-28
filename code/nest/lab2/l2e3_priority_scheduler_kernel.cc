#include <cstring>
#include "system.h"

#ifndef THREAD_NUM
#define THREAD_NUM 10
#endif

void stub(void *p)
{
    int which = (int)p;
    DEBUG('n', "Thread %d runs successfully\n", which);
}

int Nest(void *arg) {
    DEBUG('n', "Entering Nest()\n");
    char* threadNames[THREAD_NUM+1];
    threadNames[0] = "main";
    currentThread->setPriority(9);

    for (int i = 1; i <= THREAD_NUM; i += 2) 
    {
        threadNames[i] = new char[10];
        sprintf(threadNames[i], "thread%d", i);
        Thread *t = new Thread(threadNames[i]);
        t->setPriority(i);
        t->Fork(stub, (void*)i);
    }

    for (int i = 2; i <= THREAD_NUM; i += 2) 
    {
        threadNames[i] = new char[10];
        sprintf(threadNames[i], "thread%d", i);
        Thread *t = new Thread(threadNames[i]);
        t->setPriority(i);
        t->Fork(stub, (void*)i);
    }

    currentThread->Yield();

    return 0;
}