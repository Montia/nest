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
    DEBUG('e', "Thread %d starts successfully\n", which);
    work(WORK_TIME);
    DEBUG('e', "Thread %d ends successfully\n", which);
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
    return 0;
}