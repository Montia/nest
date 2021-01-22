#include <cstring>
#include "system.h"
#include "filesys.h"

#ifndef THREAD_NUM
#define THREAD_NUM 1
#endif

void run(void *p)
{
    int ret;
    char dir1[] = "/dir1";
    ret = fileSystem->Mkdir(dir1);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Mkdir(%s) returns FALSE.\n", dir1);
        return;
    }

    char file2[] = "/file2";
    ret = fileSystem->Create(file2);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Create(%s) returns FALSE.\n", file2);
        return;
    }

    char dir11[] = "/dir1/dir1-1";
    ret = fileSystem->Mkdir(dir11);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Mkdir(%s) returns FALSE.\n", dir11);
        return;
    }

    char file12[] = "/dir1/file1-2";
    ret = fileSystem->Create(file12);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Create(%s) returns FALSE.\n", file12);
        return;
    }

    char dir111[] = "/dir1/dir1-1/dir1-1-1";
    ret = fileSystem->Mkdir(dir111);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Mkdir(%s) returns FALSE.\n", dir111);
        return;
    }

    char file112[] = "/dir1/dir1-1/file1-1-2";
    ret = fileSystem->Create(file112);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Create(%s) returns FALSE.\n", file112);
        return;
    }

    struct FileAttr attr;
    ret = fileSystem->GetAttr(dir1, &attr);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->GetAttr() returns FALSE.\n");
        return;
    }
    DEBUG('e', "fileSystem->GetAttr(%s) succeeded, type: %d, ctime: %d, mtime: %d, atime: %d\n",
        dir1, attr.type, attr.createTime, attr.modifyTime, attr.accessTime);

    ret = fileSystem->GetAttr(file2, &attr);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->GetAttr() returns FALSE.\n");
        return;
    }
    DEBUG('e', "fileSystem->GetAttr(%s) succeeded, type: %d, ctime: %d, mtime: %d, atime: %d\n",
        file2, attr.type, attr.createTime, attr.modifyTime, attr.accessTime);

    ret = fileSystem->GetAttr(dir11, &attr);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->GetAttr() returns FALSE.\n");
        return;
    }
    DEBUG('e', "fileSystem->GetAttr(%s) succeeded, type: %d, ctime: %d, mtime: %d, atime: %d\n",
        dir11, attr.type, attr.createTime, attr.modifyTime, attr.accessTime);

    ret = fileSystem->GetAttr(file12, &attr);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->GetAttr() returns FALSE.\n");
        return;
    }
    DEBUG('e', "fileSystem->GetAttr(%s) succeeded, type: %d, ctime: %d, mtime: %d, atime: %d\n",
        file12, attr.type, attr.createTime, attr.modifyTime, attr.accessTime);

    ret = fileSystem->GetAttr(dir111, &attr);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->GetAttr() returns FALSE.\n");
        return;
    }
    DEBUG('e', "fileSystem->GetAttr(%s) succeeded, type: %d, ctime: %d, mtime: %d, atime: %d\n",
        dir111, attr.type, attr.createTime, attr.modifyTime, attr.accessTime);

    ret = fileSystem->GetAttr(file112, &attr);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->GetAttr() returns FALSE.\n");
        return;
    }
    DEBUG('e', "fileSystem->GetAttr(%s) succeeded, type: %d, ctime: %d, mtime: %d, atime: %d\n",
        file112, attr.type, attr.createTime, attr.modifyTime, attr.accessTime);

    char str[] = "hello, filesys!";
    OpenFile* file = fileSystem->Open(file112);
    if (file == NULL)
    {
        DEBUG('e', "fileSystem->Open() returns NULL.\n");
        return;
    }
    DEBUG('e', "Write string %s to file\n", str);
    ret = file->WriteAt(str, sizeof(str), 0);
    
    memset(str, 0, sizeof(str));
    ret = file->ReadAt(str, sizeof(str), 0);
    DEBUG('e', "Read string %s from file\n", str);
    delete file;

    char dir01[] = "/noncreate/dir";
    ret = fileSystem->Mkdir(dir01);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Mkdir(%s) returns FALSE.\n", dir01);
    }

    char file02[] = "/dir1/noncreate/file";
    ret = fileSystem->Create(file02);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Create(%s) returns FALSE.\n", file02);
    }

    char dir03[] = "/file2/dir";
    ret = fileSystem->Mkdir(dir03);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Mkdir(%s) returns FALSE.\n", dir03);
    }

    char file04[] = "/dir1/file12/file";
    ret = fileSystem->Create(file04);
    if (ret == FALSE)
    {
        DEBUG('e', "fileSystem->Create(%s) returns FALSE.\n", file04);
    }
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