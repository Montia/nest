#include <cstring>
#include "system.h"
#include "synch.h"

void work(int ticks) {
    ASSERT(interrupt->getLevel() == IntOn);
    for (int i = 0; i < ticks/10; i++) {
        interrupt->SetLevel(IntOff);
        interrupt->SetLevel(IntOn);
    }
}

KFIFO kfifo(5);
char transfered_string[] = "hello world, hello kfifo!";

void reader(void *p)
{
    // int arg = (int)p;
    // int workload = arg * 100;
    DEBUG('e', "%s begins\n", currentThread->getName());
    int string_length = strlen(transfered_string);
    int num = 0;
    for (int i = 0; i < string_length; i += num)
    {
        char buf[5];
        num = kfifo.out(buf, min(4, string_length-i));
        buf[num] = '\0';
        DEBUG('e', "%s reads %d bytes in kfifo: %s\n", currentThread->getName(), num, buf);
        work(200);
    }
}

void writer(void *p)
{
    // int arg = (int)p;
    // int workload = arg * 100;
    DEBUG('e', "%s begins\n", currentThread->getName());
    int string_length = strlen(transfered_string);
    int num = 0;
    for (int i = 0; i < string_length; i += num)
    {
        num = kfifo.in(transfered_string+i, min(3, string_length-i));
        char buf[4];
        buf[num] = '\0';
        memcpy(buf, transfered_string+i, num);
        DEBUG('e', "%s writes %d bytes in kfifo: %s\n", currentThread->getName(), num, buf);
        work(200);
    }
}

int Nest(void *arg) {
    DEBUG('e', "Entering Nest()\n");
    char* threadNames[3];
    threadNames[0] = "main";

    for (int i = 1; i <= 2; i++) 
    {
        threadNames[i] = new char[10];
        sprintf(threadNames[i], "thread%d", i);
        Thread *t = new Thread(threadNames[i]);
        if (i % 2 == 0)
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