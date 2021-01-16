import re
from collections import namedtuple
from collections import OrderedDict
from operator import attrgetter
# import sys
# raise Exception(str(sys.path))
from parse_result import *

def is_read(line):
    a = re.findall("(.*) reads (.*) bytes in kfifo: (.*)\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_write(line):
    a = re.findall("(.*) writes (.*) bytes in kfifo: (.*)", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def check(lines):
    read_string = ''
    write_string = ''
    for line_num, line in enumerate(lines):
        ret = is_read(line)
        if ret is not None:
            _, _, s = ret
            read_string += s
            if len(read_string) > len(write_string):
                error_message = 'Error in line {}: \
                    Reader reads "{}" from kfifo, \
                    but writer only writes {} for now.'\
                    .format(line_num+1, read_string, write_string)
                return False, error_message
            continue
            
        ret = is_write(line)
        if ret is not None:
            _, _, s = ret
            write_string += s
            continue
    
    if read_string != write_string:
        error_message = 'Writer writes "{}" in kfifo, but reader reads "{}"'\
            .format(write_string, read_string)
        return False, error_message
    else:
        return True, None
