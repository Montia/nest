#include <cstring>
#include "system.h"
#include "filesys.h"
#include "disk.h"

#ifndef THREAD_NUM
#define THREAD_NUM 1
#endif

#define INDIRECT_BLOCK_DATA (SectorSize / 4 * SectorSize)
char str[INDIRECT_BLOCK_DATA+SectorSize+1];

void run(void *p)
{
    int ret;
    ret = fileSystem->Create("hello_filesys");
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Create() returns FALSE.\n");
        return;
    }
    fileSystem->Print();

    OpenFile* file = fileSystem->Open("hello_filesys");
    if (file == NULL)
    {
        DEBUG('e', "fileSystem->Open() returns NULL.\n");
        return;
    }

    const char copy[33] = "This is a string of length 32...";
    for (int i = 0; i < (INDIRECT_BLOCK_DATA+SectorSize) / 32; i++)
    {
        strncat(str, copy, 32);
    }
    int length = strlen(str);
    DEBUG('e', "Write string (length %d) \"%s\" to file\n", length, str);
    ret = file->WriteAt(str, length, 0);
    
    memset(str, 0, sizeof(str));
    ret = file->ReadAt(str, length, 0);
    DEBUG('e', "Read string \"%s\" from file\n", str);
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