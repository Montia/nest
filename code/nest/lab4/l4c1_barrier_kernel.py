import re
from collections import namedtuple
from collections import OrderedDict
from operator import attrgetter
# import sys
# raise Exception(str(sys.path))
from parse_result import *

def is_starts_working(line):
    a = re.findall("(.*) starts working for phase (.*)\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_ends_working(line):
    a = re.findall("(.*) ends working for phase (.*)\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_post_called(line):
    a = re.findall("postPhaseAction is called in phase (.*)\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def check(lines):
    holder = None
    THREAD_NUM = 3
    PHASE_NUM = 3
    finished = 0
    post_called = 0
    for line_num, line in enumerate(lines):
        ret = is_starts_working(line)
        if ret is not None:
            name, phase = ret
            phase = int(phase)
            if phase > post_called:
                error_message = 'Error in line {}: \
                    {} starts working for phase {}, \
                    but phase {}\'s postPhaseAction hasn\'t been called.'\
                    .format(line_num+1, name, phase, post_called)
                return False, error_message
            continue

        ret = is_ends_working(line)
        if ret is not None:
            name, phase = ret
            phase = int(phase)
            finished += 1
            continue
            
        ret = is_post_called(line)
        if ret is not None:
            phase = int(ret)
            if phase != post_called:
                error_message = "Error in line {}: \
                    Phase {}'s postPhaseAction is called, \
                    but phase {}'s hasn't been called."\
                    .format(line_num+1, phase, post_called)
                return False, error_message
            elif finished != THREAD_NUM:
                error_message = "Error in line {}: \
                    Phase {}'s postPhaseAction is called, \
                    but {}/{} threads finished working."\
                    .format(line_num+1, phase, finished, THREAD_NUM)
                return False, error_message
            finished = 0
            post_called += 1
            continue
    
    if post_called == PHASE_NUM:
        return True, None
    else:
        error_message = 'Error in line {}: \
            There are {} phases, but postPhaseAction is called {} times.'\
            .format(line_num+1, THREAD_NUM, finished)
        return False, error_message
