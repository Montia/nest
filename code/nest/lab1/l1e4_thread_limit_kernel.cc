#include <cstring>
#include "system.h"

#ifndef THREAD_NUM_LIMIT
#define THREAD_NUM_LIMIT 128
#endif

void stub(void *p)
{
    int which = (int)p;
    DEBUG('n', "Thread %d runs successfully\n", which);
}

int Nest(void *arg) {
    DEBUG('n', "Entering Nest()\n");
    char* threadNames[THREAD_NUM_LIMIT+1];
    threadNames[0] = "main";

    for (int i = 1; i < THREAD_NUM_LIMIT; i++) 
    {
        threadNames[i] = new char[10];
        sprintf(threadNames[i], "thread%d", i);
        Thread *t = new Thread(threadNames[i]);
        int ret = t->Fork(stub, (void*)i);
        if (ret != 0) {
            DEBUG('n', "Forking %s failed!\n", threadNames[i]);
            return -1;
        } else {
            DEBUG('n', "Forking %s succeeded.\n", threadNames[i]);
        }
    }
    threadNames[THREAD_NUM_LIMIT] = new char[10];
    sprintf(threadNames[THREAD_NUM_LIMIT], "thread%d", THREAD_NUM_LIMIT);
    Thread *t = new Thread(threadNames[THREAD_NUM_LIMIT]);
    int ret = t->Fork(stub, (void*)THREAD_NUM_LIMIT);
    if (ret == 0) {
        DEBUG('n', "Forking %s succeeded, but over limit\n", threadNames[THREAD_NUM_LIMIT]);
        return -1;
    }
    return 0;
}
