#include "machine.h"
#include "vm.h"

bool occupied[NumPhysPages];

int Nest(void *arg) 
{
    for (int i = 1; i <= NumPhysPages+1; i++)
    {
        int page = get_and_use_page();
        DEBUG('e', "get_and_use_page() returns %d\n", page);
        if (page < 0)
        {
            if (i == NumPhysPages + 1)
            {
                continue;
            }
            else
            {
                for (int j = 0; j < NumPhysPages; j++)
                {
                    if (!occupied[j])
                    {
                        DEBUG('e', "get_and_use_page() returned %d, but page %d is still unoccupied.\n", page, j);
                        // return false;
                        break;
                    }
                }
            }
        }
        else
        {
            if (page >= NumPhysPages)
            {
                DEBUG('e', "Page returned by get_and_use_page() should be less than NumPhysPages(%d).\n", NumPhysPages);
                // return false;
            }
            if (occupied[page])
            {
                DEBUG('e', "get_and_use_page() returned %d, but it has been occupied.\n", page);
                // return false
            }
            occupied[page] = true;
        }
    }

    int free_page_num = 0;
    for (int i = 1; i <= NumPhysPages; i += 3)
    {
        free_page(i);
        occupied[i] = false;
        free_page_num++;
        DEBUG('e', "free_page(%d).\n", i);
    }

    for (int i = 1; i <= free_page_num+1; i++)
    {
        int page = get_and_use_page();
        DEBUG('e', "get_and_use_page() returns %d\n", page);
        if (page < 0)
        {
            if (i == NumPhysPages + 1)
            {
                continue;
            }
            else
            {
                for (int j = 0; j < NumPhysPages; j++)
                {
                    if (!occupied[j])
                    {
                        DEBUG('e', "get_and_use_page() returned %d, but page %d is still unoccupied.\n", page, j);
                        // return false;
                        break;
                    }
                }
            }
        }
        else
        {
            if (page >= NumPhysPages)
            {
                DEBUG('e', "Page returned by get_and_use_page() should be less than NumPhysPages(%d).\n", NumPhysPages);
                // return false;
            }
            if (occupied[page])
            {
                DEBUG('e', "get_and_use_page() returned %d, but it has been occupied.\n", page);
                // return false;
            }
            occupied[page] = true;
        }
    }
    return 0;
}