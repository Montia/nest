import re
from collections import namedtuple
from collections import OrderedDict
from operator import attrgetter
# import sys
# raise Exception(str(sys.path))
from parse_result import *

def is_acquired_lock(line):
    a = re.findall("(.*) acquired lock\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_finished_work(line):
    a = re.findall("(.*) finished work\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def check(lines):
    holder = None
    THREAD_NUM = 3
    finished = 0
    for line_num, line in enumerate(lines):
        ret = is_acquired_lock(line)
        if ret is not None:
            name = ret
            if holder is not None:
                error_message = 'Error in line {}: \
                    {} acquired lock while {} holds it'\
                    .format(line_num+1, name, holder)
                return False, error_message
            else:
                holder = name
            continue
            
        ret = is_finished_work(line)
        if ret is not None:
            name = ret
            if holder != name:
                error_message = 'Error in line {}: \
                    {} hasn\'t released lock, but {} holds it'\
                    .format(line_num+1, name, holder)
                return False, error_message
            else:
                finished += 1
                holder = None
            continue
    
    if finished == THREAD_NUM:
        return True, None
    else:
        error_message = 'Error in line {}: \
            There are {} working threads, but {} finished working'\
            .format(line_num+1, THREAD_NUM, finished)
        return False, error_message
