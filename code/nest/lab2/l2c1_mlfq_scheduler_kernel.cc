#include <cstring>
#include "system.h"

#ifndef THREAD_NUM
#define THREAD_NUM 3
#endif

#ifndef PRINT_NUM
#define PRINT_NUM 2
#endif

void PrintUid(void *p)
{
    int which = (int)p;
    for (int i = 0; i < PRINT_NUM; i++)
    {
	    DEBUG('n', "*** thread %d's uid is %d ***\n", which, GetUid());
        currentThread->Yield();
    }
}

int Nest(void *arg) {
    DEBUG('n', "Entering Nest()\n");
    char* threadNames[THREAD_NUM+1];
    threadNames[0] = "main";

    PrintUid(0);
    for (int i = 1; i <= THREAD_NUM; i++) 
    {
        threadNames[i] = new char[10];
        sprintf(threadNames[i], "thread%d", i);
        Thread *t = new Thread(threadNames[i]);
        t->Fork(PrintUid, (void*)i);
    }
    for (int i = 1; i <= THREAD_NUM; i++) 
    {
        delete[] threadNames[i];
    }
    return 0;
}