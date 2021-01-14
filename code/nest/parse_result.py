import re

# return old and new interrupt levels in a tuple ("off" or "on")
def is_turn_interrupts(line):
    a = re.findall('\tinterrupts: (.*) -> (.*)\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return tick value
def is_tick(line):
    a = re.findall('== Tick (.*) ==', line)
    if (len(a) > 0):
        return int(a[0])
    else:
        return None

# return tick and interrupt level in a tuple before dumping interrupts
def is_before_dump_interrupts(line):
    a = re.findall('Time: (.*), interrupts (.*)\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return true if it's the beginning of pending interrupts
def is_dump_interrupts_beginning(line):
    a = re.findall('Pending interrupts:\n', line)
    if (len(a) > 0):
        return True
    else:
        return None

# return interrupt handler and scheduling point of a pending interrupt in a tuple
def is_pending_interrupt(line):
    a = re.findall('Interrupt handler (.*), scheduled at (.*)\n', line)
    if (len(a) > 0):
        return True
    else:
        return None

# return true if it's the ending of pending interrupts
def is_dump_interrupts_ending(line):
    a = re.findall('End of pending interrupts\n', line)
    if (len(a) > 0):
        return True
    else:
        return None

# return the name of yielding thread without double quotes
def is_yield_thread(line):
    a = re.findall('Yielding thread "(.*)"\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return forking thread's name, function, arg in a tuple
def is_fork_thread(line):
    a = re.findall(\
        'Forking thread "(.*)" with func = (.*), arg = (.*)\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return put thread's name
def is_put_thread_on_ready_list(line):
    a = re.findall(\
        'Putting thread (.*) on ready list.\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return sleeping thread's name
def is_sleep_thread(line):
    a = re.findall(\
        'Sleeping thread "(.*)"\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return old and new thread's name during thread switching
def is_switch_thread(line):
    a = re.findall(\
        'Switching from thread "(.*)" to thread "(.*)"\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return thread's name after thread switching
def is_after_switch_thread(line):
    a = re.findall('Now in thread "(.*)"\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return finished thread's name
def is_finish_thread(line):
    a = re.findall('Finishing thread "(.*)"\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return deleted thread's name
def is_delete_thread(line):
    a = re.findall('Deleting thread "(.*)"\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return true if machine is idle
def is_machine_idle_without_interrupts(line):
    a = re.findall('Machine idle.  No interrupts to do.\n', line)
    if (len(a) > 0):
        return True
    else:
        return None

# return true if machine is halting
def is_unexpected_exception(line):
    a = re.findall('Unexpected user mode exception (.*) (.*)\n', line)
    if (len(a) > 0):
        return int(a[0][0]), int(a[0][1])
    else:
        return None

# return true if machine is halting
def is_user_program_exit(line):
    a = re.findall('User program exits with code (.*).\n', line)
    if (len(a) > 0):
        return int(a[0])
    else:
        return None

# return true if machine is halting
def is_machine_halt(line):
    a = re.findall('Machine halting!\n', line)
    if (len(a) > 0):
        return True
    else:
        return None

# return total/idle/system/user ticks in a tuple
def is_tick_summary(line):
    a = re.findall(\
        'Ticks: total (.*), idle (.*), system (.*), user (.*)\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return disk read/write in a tuple
def is_disk_summary(line):
    a = re.findall(\
        'Disk I/O: reads (.*), writes (.*)\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return console read/write in a tuple
def is_console_summary(line):
    a = re.findall(\
        'Console I/O: reads (.*), writes (.*)\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return paging fault num
def is_paging_summary(line):
    a = re.findall(\
        'Paging: faults (.*)\n', line)
    if (len(a) > 0):
        return int(a[0])
    else:
        return None

# return network received/sent in a tuple
def is_network_summary(line):
    a = re.findall(\
        'Network I/O: packets received (.*), sent (.*)\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

# return true if machine is cleaning up
def is_clean_up(line):
    a = re.findall('Cleaning up...\n', line)
    if (len(a) > 0):
        return True
    else:
        return None
