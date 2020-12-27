#include <cstring>
#include "system.h"

#ifndef THREAD_NUM
#define THREAD_NUM 3
#endif

#ifndef TS_NUM
#define TS_NUM 2
#endif

void call_ts(void* p)
{
    int which = (int)p;
    for (int i = 0; i < TS_NUM; i++)
    {
        DEBUG('n', "Call ts() from thread %d\n", which);
	    ts();
        currentThread->Yield();
    }
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
        int ret = t->Fork(call_ts, (void*)i);
        if (ret != 0) 
        {
            DEBUG('n', "Forking thread %s failed!", threadNames[i]);
            return -1;
        }
    }
    currentThread->Yield();
    return 0;
}
