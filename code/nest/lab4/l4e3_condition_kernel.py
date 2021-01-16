import re
from collections import namedtuple
from collections import OrderedDict
from operator import attrgetter
# import sys
# raise Exception(str(sys.path))
from parse_result import *

def is_finished_waiting(line):
    a = re.findall("(.*) finished waiting\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_signaling(line):
    a = re.findall("(.*) signaling one thread\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_broadcasting(line):
    a = re.findall("(.*) broadcasting all threads\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def check(lines):
    signaled = False
    signal = 0
    broadcast = False
    finished = 0
    THREAD_NUM = 3
    for line_num, line in enumerate(lines):
        ret = is_finished_waiting(line)
        if ret is not None:
            name = ret
            if not broadcast and signaled == False:
                error_message = 'Error in line {}: \
                    {} finished waiting, but condition variable hasn\'t signaled or broadcasted'\
                    .format(line_num+1, name)
                return False, error_message
            elif not broadcast and signal <= 0:
                error_message = 'Error in line {}: \
                    {} finished waiting, but condition variable hasn\'t broadcasted, and one thread has been signaled'\
                    .format(line_num+1, name)
                return False, error_message
            else:
                finished += 1
                signal -= 1
            continue

        ret = is_signaling(line)
        if ret is not None:
            signal += 1
            signaled = True
            continue
            
        ret = is_broadcasting(line)
        if ret is not None:
            broadcast = True
            continue
    
    if finished == THREAD_NUM:
        return True, None
    else:
        error_message = 'There are {} working threads, but {} finished working'\
            .format(THREAD_NUM, finished)
        return False, error_message
