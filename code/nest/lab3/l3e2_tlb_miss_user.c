#include "syscall.h"

#ifndef VEC_LENGTH
#define VEC_LENGTH 10
#endif

int a[VEC_LENGTH];
int b[VEC_LENGTH];
int c;

int main() 
{
    int i;
    for (i = 0; i < VEC_LENGTH; i++)
    {
        a[i] = i;
        b[i] = i;
    }
    for (i = 0; i < VEC_LENGTH; i++)
    {
        c += a[i] * b[i];
    }
    Exit(c);
}