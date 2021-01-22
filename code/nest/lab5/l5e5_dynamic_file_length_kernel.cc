#include <cstring>
#include "system.h"
#include "filesys.h"

#ifndef THREAD_NUM
#define THREAD_NUM 1
#endif

#ifndef WRITE_NUM
#define WRITE_NUM 3
#endif

void run(void *p)
{
    int ret;
    ret = fileSystem->Create("hello_filesys", 1);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Create() returns FALSE.\n");
        return;
    }
    fileSystem->Print();

    char str[] = "hello, filesys!";
    int length = strlen(str);
    OpenFile* file = fileSystem->Open("hello_filesys");
    if (file == NULL)
    {
        DEBUG('e', "fileSystem->Open() returns NULL.\n");
        return;
    }

    for (int i = 0; i < WRITE_NUM; i++)
    {
        DEBUG('e', "Write string %s to file\n", str);
        ret = file->Write(str, length);
        DEBUG('e', "Current file length: %d\n", file->Length());
    }
    
    char bigstr[sizeof(str)*WRITE_NUM];
    memset(bigstr, 0, sizeof(bigstr));
    ret = file->ReadAt(bigstr, sizeof(bigstr), 0);
    DEBUG('e', "Read string %s from file\n", bigstr);
    DEBUG('e', "Read string returns %d\n", ret);
    delete file;
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

    currentThread->Yield();

    return 0;
}