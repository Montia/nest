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
    DEBUG('e', "Entering main\n");
    (void) Initialize(argc, argv);
    
#ifdef TEST_IN_KERNEL
	void *arg = NULL;
	// TODO: construct arg according to argc and argv
    Nest(arg);
#else
    int argCount;
    for (argc--, argv++; argc > 0; argc -= argCount, argv += argCount) {
	    argCount = 1;
        if (!strcmp(*argv, "-x")) {        	// run a user program
	        ASSERT(argc > 1);
            DEBUG('e', "Identify -x %s\n", *(argv+1));
            StartProcess(*(argv + 1));
            argCount = 2;
        } 
    }
#endif

    currentThread->Finish();
	// Not reached...
}
