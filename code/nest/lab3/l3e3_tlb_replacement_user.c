#include "syscall.h"

#ifndef MATRIX_M
#define MATRIX_M 2
#endif

int a[MATRIX_M][32];
int b[32][MATRIX_M];
int c[MATRIX_M][MATRIX_M];

int main() 
{
    int i, j, k, sum;
    for (i = 0; i < MATRIX_M; i++)
    for (j = 0; j < 32; j++)
    {
        a[i][j] = i*32+j;
        b[j][i] = j*MATRIX_M+i;
    }
    for (i = 0; i < MATRIX_M; i++)
    for (j = 0; j < MATRIX_M; j++)
    for (k = 0; k < 32; k++)
    {
        c[i][j] += a[i][k] * b[k][j];
    }
    for (i = 0; i < MATRIX_M; i++)
    for (j = 0; j < MATRIX_M; j++)
    {
        sum += c[i][j];
    }
    Exit(sum);
}