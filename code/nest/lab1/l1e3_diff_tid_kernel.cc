#include <cstring>
#include "system.h"

#ifndef THREAD_NUM
#define THREAD_NUM 3
#endif

#ifndef PRINT_NUM
#define PRINT_NUM 2
#endif

void PrintTid(int which)
{
    for (int i = 0; i < PRINT_NUM; i++)
    {
	    DEBUG('n', "*** thread %d's tid is %d ***\n", which, GetTid());
        currentThread->Yield();
    }
}

int Nest(void *arg) {
    DEBUG('n', "Entering Nest()\n");
    ASSERT(THREAD_NUM < 10);

    PrintTid(0);
    for (int i = 1; i <= THREAD_NUM; i++) 
    {
        char *threadName = new char[10];
        strcpy(threadName, "thread1");
        threadName[6] = i+'0';
        Thread *t = new Thread(threadName);
        t->Fork(PrintTid, (void*)i);
    }
}