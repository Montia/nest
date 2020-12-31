#include <cstring>
#include "system.h"

#ifndef THREAD_NUM
#define THREAD_NUM 3
#endif

#ifndef WORK_TIME
#define WORK_TIME 500
#endif

void work(int ticks) {
    ASSERT(interrupt->getLevel() == IntOn);
    for (int i = 0; i < ticks/10; i++) {
        interrupt->SetLevel(IntOff);
        interrupt->SetLevel(IntOn);
    }
}

void run(void *p)
{
    int which = (int)p;
    DEBUG('n', "Thread %d starts successfully\n", which);
    if (which <= THREAD_NUM)
    {
        work(WORK_TIME*(THREAD_NUM+2-which));
    }
    else
    {
        work(200);
    }
    
    if (which == THREAD_NUM)
    {
        for (int i = 1; i <= THREAD_NUM; i++)
        {
            char* threadNames = new char[10];
            sprintf(threadNames, "thread%d", THREAD_NUM+i);
            Thread *t = new Thread(threadNames);
            t->Fork(run, (void*)(THREAD_NUM+i));
        }
    }
    DEBUG('n', "Thread %d ends successfully\n", which);
}

int Nest(void *arg) {
    DEBUG('n', "Entering Nest()\n");
    char* threadNames[THREAD_NUM+1];
    threadNames[0] = "main";

    for (int i = 1; i <= THREAD_NUM; i++) 
    {
        threadNames[i] = new char[10];
        sprintf(threadNames[i], "thread%d", i);
        Thread *t = new Thread(threadNames[i]);
        t->Fork(run, (void*)i);
    }
    return 0;
}