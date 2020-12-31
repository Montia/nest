import re
from collections import OrderedDict
from parse_result import *
from operator import attrgetter

def is_set_queue_num(line):
    a = re.findall("MQFS scheduler's queue_num is set to (.*)\n", line)
    if (len(a) > 0):
        return int(a[0])
    else:
        return None

def is_set_qslice(line):
    a = re.findall("Queue (.*)'s time slice is set to (.*)\n", line)
    if (len(a) > 0):
        return int(a[0][0]), int(a[0][1])
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
            self.q = 0
            self.remaining_slice = 0
        
        def __str__(self):
            return 'Thread(name={!s}, status={!s}, starts_run={!s}, queue={!s})'\
                .format(self.name, self.status, self.starts_run, str(self.q+1))
        
        def __repr__(self):
            return str(self)

    current_threads = OrderedDict()
    current_threads['main'] = Thread('main', 'Running')
    running_thread = current_threads['main']
    running_thread.starts_run = 0
    yielding_thread = None
    fork_thread_name = None
    queue_num = None
    qslices = []
    tick = 0
    for line_num, line in enumerate(lines):
        ret = is_set_queue_num(line)
        if ret is not None:
            queue_num = ret
            continue

        ret = is_set_qslice(line)
        if ret is not None:
            qslices.append(ret[1])
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
            current_threads[name] = Thread(name)
            current_threads[name].remaining_slice = qslices[0]
            continue
        
        ret = is_switch_thread(line)
        if ret is not None:
            prior, name = ret
            if name not in current_threads:
                error_message = 'Error in line {}: \
                    Unknown thread {} is Running'\
                    .format(line_num+1, name)
                return False, error_message
            
            runnable_threads = [t for t in current_threads.values() \
                if t.status in ['Running', 'Ready']]
            if running_thread.status in ['Ready', 'Running'] \
                and running_thread.q <= min(runnable_threads, key=attrgetter('q')).q \
                and tick - running_thread.starts_run < running_thread.remaining_slice - 20:
                error_message = 'Error in line {}: \
                    Thread {} should not be switched that early'\
                    .format(line_num+1, running_thread)
                return False, error_message

            if running_thread.q < queue_num - 1:
                running_thread.remaining_slice -= tick - running_thread.starts_run
                if running_thread.remaining_slice <= 0:
                    running_thread.q += 1
                    running_thread.remaining_slice = qslices[running_thread.q]
            else:
                running_thread.remaining_slice = qslices[running_thread.q]
            
            running_thread.starts_run = None
            current_threads[name].status = 'Running'
            running_thread = current_threads[name]
            running_thread.starts_run = tick

            runnable_threads = [t for t in current_threads.values() \
                if t.status in ['Running', 'Ready']]
            min_q_thread = min(runnable_threads, key=attrgetter('q'))
            if running_thread.q > min_q_thread.q:
                error_message = 'Error in line {}: \
                    Thread {} should be switched in last timer handler,\
                    because thread {} is in higher priority queue.'\
                    .format(line_num+1, running_thread, min_q_thread)
                return False, error_message

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
            if tick - running_thread.starts_run > running_thread.remaining_slice + timer_interval + 10:
                if running_thread.q < queue_num - 1:
                    running_thread.q += 1
                    running_thread.remaining_slice = \
                        qslices[running_thread.q] - (tick - running_thread.starts_run - running_thread.remaining_slice)
                    running_thread.starts_run = tick
                    runnable_threads = [t for t in current_threads.values() \
                        if t.status in ['Running', 'Ready']]
                    min_q_thread = min(runnable_threads, key=attrgetter('q'))
                    if running_thread.q > min_q_thread.q:
                        error_message = 'Error in line {}: \
                            Thread {} should be switched in last timer handler,\
                            because thread {} is in higher priority queue.'\
                            .format(line_num+1, running_thread, min_q_thread)
                        return False, error_message
                else:
                    error_message = 'Error in line {}: \
                        Thread {} should be switched in last timer handler.'\
                        .format(line_num+1, running_thread, min_q_thread)
                    return False, error_message

        
        ret = is_yield_thread(line)
        if ret is not None:
            name = ret
            yielding_thread = current_threads[name]
            continue
    
    return True, None

