import re
from collections import OrderedDict
from parse_result import *

def is_set_rr_slice(line):
    a = re.findall("RR scheduler's time slice is set to (.*)\n", line)
    if (len(a) > 0):
        return int(a[0])
    else:
        return None

def is_set_timer_interval(line):
    a = re.findall("Timer's interval is set to (.*)", line)
    if (len(a) > 0):
        return int(a[0])
    else:
        return None

def check(lines):
    class Thread:
        def __init__(self, name, status=None):
            self.name = name
            self.status = status
            self.starts_run = None
        
        def __str__(self):
            return 'Thread(name={!s}, status={!s}, starts_run={!s})'\
                .format(self.name, self.status, self.starts_run)
        
        def __repr__(self):
            return str(self)

    current_threads = OrderedDict()
    current_threads['main'] = Thread('main', 'Running')
    running_thread = current_threads['main']
    running_thread.starts_run = 0
    yielding_thread = None
    fork_thread_name = None
    tick = 0
    for line_num, line in enumerate(lines):
        ret = is_set_rr_slice(line)
        if ret is not None:
            time_slice = ret
            continue

        ret = is_set_timer_interval(line)
        if ret is not None:
            timer_interval = ret
            continue

        ret = is_put_thread_on_ready_list(line)
        if ret is not None:
            name = ret
            current_threads.setdefault(name, Thread(name)).status = 'Ready'
            continue

        ret = is_fork_thread(line)
        if ret is not None:
            name, _, _ = ret
            fork_thread_name = name
            continue
        
        ret = is_switch_thread(line)
        if ret is not None:
            prior, name = ret
            if name not in current_threads:
                error_message = 'Error in line {}: \
                    Unknown thread {} is Running'\
                    .format(line_num+1, name)
                return False, error_message
            
            if running_thread.status in ['Ready', 'Running'] \
                and tick - running_thread.starts_run < time_slice - 20:
                error_message = 'Error in line {}: \
                    Thread {} should not be switched that early'\
                    .format(line_num+1, running_thread)
                return False, error_message
            
            current_threads[name].status = 'Running'
            running_thread.starts_run = None
            running_thread = current_threads[name]
            running_thread.starts_run = tick
            if yielding_thread is not None and prior != yielding_thread.name:
                yielding_thread = None
            continue
        
        ret = is_sleep_thread(line)
        if ret is not None:
            name = ret
            if name not in current_threads:
                error_message = 'Error in line {}: \
                    Unknown thread {} is Blocked'\
                    .format(line_num+1, name)
                return False, error_message
            current_threads[name].status = 'Blocked'
            continue
        
        ret = is_delete_thread(line)
        if ret is not None:
            name = ret
            if name not in current_threads:
                error_message = 'Error in line {}: \
                    Unknown thread {} is deleted'\
                    .format(line_num+1, name)
                return False, error_message
            del current_threads[name]
            continue
        
        ret = is_tick(line)
        if ret is not None:
            tick = ret
            if tick - running_thread.starts_run > time_slice + timer_interval + 10:
                error_message = 'Error in line {}: \
                    Thread {} should be switched in last timer handler'\
                    .format(line_num+1, name)
                return False, error_message
        
        ret = is_yield_thread(line)
        if ret is not None:
            name = ret
            yielding_thread = current_threads[name]
            continue
    
    return True, None

