import re
from collections import namedtuple
from collections import OrderedDict
from operator import attrgetter
# import sys
# raise Exception(str(sys.path))
from parse_result import *

def is_reader_aqcquired(line):
    a = re.findall("(.*) acquired reader lock\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_reader_released(line):
    a = re.findall("(.*) released reader lock\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_writer_aqcquired(line):
    a = re.findall("(.*) acquired writer lock\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_writer_released(line):
    a = re.findall("(.*) released writer lock\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def check(lines):
    writer_holder = None
    reader_holder = set()
    max_reader_num = 0
    THREAD_NUM = 10
    thread_end = 0
    for line_num, line in enumerate(lines):
        ret = is_reader_aqcquired(line)
        if ret is not None:
            name = ret
            if writer_holder is not None:
                error_message = 'Error in line {}: \
                    {} acquired reader lock, \
                    but {} holds writer lock now.'\
                    .format(line_num+1, name, writer_holder)
                return False, error_message
            reader_holder.add(name)
            max_reader_num = max(max_reader_num, len(reader_holder))
            continue

        ret = is_reader_released(line)
        if ret is not None:
            name = ret
            if name not in reader_holder:
                error_message = "Error in line {}: \
                    {} released reader lock, \
                    but it doesn't hold it now."\
                    .format(line_num+1, name)
                return False, error_message
            reader_holder.remove(name)
            thread_end += 1
            continue
            
        ret = is_writer_aqcquired(line)
        if ret is not None:
            name = ret
            if writer_holder is not None:
                error_message = 'Error in line {}: \
                    {} acquired writer lock, \
                    but {} holds writer lock now.'\
                    .format(line_num+1, name, writer_holder)
                return False, error_message
            if len(reader_holder) > 0:
                error_message = 'Error in line {}: \
                    {} acquired writer lock, \
                    but {} holds reader lock now.'\
                    .format(line_num+1, name, sorted(reader_holder))
                return False, error_message
            writer_holder = name
            continue

        ret = is_writer_released(line)
        if ret is not None:
            name = ret
            if name != writer_holder:
                error_message = "Error in line {}: \
                    {} released writer lock, \
                    but it doesn't hold it now."\
                    .format(line_num+1, name)
                return False, error_message
            writer_holder = None
            thread_end += 1
            continue
    
    if max_reader_num < 4:
        error_message = 'Your ReaderWriterLock seems not supporting reader sharing well.'
        return False, error_message
    elif THREAD_NUM != thread_end:
        error_message = '{}/{} threads end'.format(thread_end, THREAD_NUM)
        return False, error_message
    else:
        return True, None
