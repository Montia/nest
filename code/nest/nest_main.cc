//  nest_main.cc 
//	Bootstrap code to initialize the operating system kernel, then run a test.
//
//	Allows direct calls into internal operating system functions,
//	or start a user program.

#include "utility.h"
#include "system.h"

#ifdef TEST_IN_KERNEL
// Functions used for tests in kernel
extern int Nest(void *arg);
#else
extern void StartProcess(char *file);
#endif

int main(int argc, char **argv)
{
    int argCount;			// the number of arguments 
					// for a particular command

    DEBUG('t', "Entering main");
    (void) Initialize(argc, argv);
    
#ifdef TEST_IN_KERNEL
	void *arg = NULL;
	// TODO: construct arg according to argc and argv
    Nest(arg);
#else
	// TODO: construct arg according to argc and argv
    StartProcess(*(argv + 1));
#endif

    currentThread->Finish();
	// Not reached...
}
