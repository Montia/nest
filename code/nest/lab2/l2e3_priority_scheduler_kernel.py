import re
from collections import namedtuple
from collections import OrderedDict
from operator import attrgetter
# import sys
# raise Exception(str(sys.path))
from parse_result import *

def is_ts_call(line):
    a = re.findall('Call ts\(\) from thread (.*)\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def check(lines):
    class Thread:
        def __init__(self, name, status=None):
            self.name = name
            self.priority = int(name[len('thread'):]) \
                if name.startswith('thread') else 9
            self.status = status
        
        def __str__(self):
            return 'Thread(name={!s}, priority={!s}, status={!s})'\
                .format(self.name, self.priority, self.status)
        
        def __repr__(self):
            return str(self)

    current_threads = OrderedDict()
    current_threads['main'] = Thread('main', 'Running')
    running_thread = current_threads['main']
    yielding_thread = None
    fork_thread_name = None
    for line_num, line in enumerate(lines):
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
            current_threads[name].status = 'Running'
            running_thread = current_threads[name]
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
            runnable_threads = [t for t in current_threads.values() \
                if t.status in ['Running', 'Ready']]
            max_priority_thread = max(runnable_threads, \
                key=attrgetter('priority'))
            if max_priority_thread is not yielding_thread \
                and max_priority_thread.priority > running_thread.priority:
                if max_priority_thread.name == fork_thread_name:
                    fork_thread_name = None
                    continue
                error_message = 'Error in line {}: \
                    On tick {}, {} is running, \
                    but thread {} has higher priority'\
                    .format(line_num+1, tick, running_thread, max_priority_thread)
                return False, error_message
            if yielding_thread in runnable_threads:
                runnable_threads.remove(yielding_thread)
            if running_thread is yielding_thread and len(runnable_threads) >= 1:
                error_message = 'Error in line {}: \
                    {} shouldn\'t be scheduled after yielding \
                    if {} is runnable'\
                    .format(line_num+1, running_thread, runnable_threads)
                return False, error_message
            second_max = max(runnable_threads, key=attrgetter('priority'))
            if max_priority_thread is yielding_thread \
                and second_max.priority > running_thread.priority:
                error_message = 'Error in line {}: \
                    On tick {}, {} is running, \
                    but thread {} has higher priority'\
                    .format(line_num+1, tick, running_thread, second_max)
                return False, error_message
            continue
        
        ret = is_yield_thread(line)
        if ret is not None:
            name = ret
            yielding_thread = current_threads[name]
            continue
    
    return True, None
