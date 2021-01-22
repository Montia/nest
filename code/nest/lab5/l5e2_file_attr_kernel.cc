#include <cstring>
#include <unistd.h>
#include "system.h"
#include "filesys.h"

#ifndef THREAD_NUM
#define THREAD_NUM 1
#endif

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
    sleep(2);

    char str[] = "hello, filesys!";
    OpenFile* file = fileSystem->Open("hello_filesys");
    if (file == NULL)
    {
        DEBUG('e', "fileSystem->Open() returns NULL.\n");
        return;
    }
    DEBUG('e', "Write string %s to file\n", str);
    ret = file->WriteAt(str, sizeof(str), 0);
    sleep(2);
    
    memset(str, 0, sizeof(str));
    ret = file->ReadAt(str, sizeof(str), 0);
    DEBUG('e', "Read string %s from file\n", str);
    delete file;

    struct FileAttr attr;
    ret = fileSystem->GetAttr("hello_filesys", &attr);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->GetAttr() returns FALSE.\n");
        return;
    }
    DEBUG('e', "fileSystem->GetAttr() succeeded, type: %d, ctime: %d, mtime: %d, atime: %d\n",
        attr.type, attr.createTime, attr.modifyTime, attr.accessTime);
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