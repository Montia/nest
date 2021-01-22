import re
from collections import namedtuple
from collections import OrderedDict
from operator import attrgetter
# import sys
# raise Exception(str(sys.path))
from parse_result import *

def is_create_false(line):
    a = re.findall(r"fileSystem->Create\(\) returns FALSE.\n", line)
    if (len(a) > 0):
        return True
    else:
        return None

def is_open_null(line):
    a = re.findall(r"fileSystem->Open\(\) returns NULL.\n", line)
    if (len(a) > 0):
        return True
    else:
        return None

def is_write_string(line):
    a = re.findall("Write string \(length (.*)\) (.*) to file\n", line)
    if (len(a) > 0):
        return a[0][1]
    else:
        return None

def is_read_string(line):
    a = re.findall("Read string (.*) from file\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def check(lines):
    write_string = None
    for line_num, line in enumerate(lines):
        ret = is_create_false(line)
        if ret is not None:
            error_message = 'Error in line {}: \
                Creating file failed'\
                .format(line_num+1)
            return False, error_message

        ret = is_open_null(line)
        if ret is not None:
            error_message = 'Error in line {}: \
                Opening file failed'\
                .format(line_num+1)
            return False, error_message
            
        ret = is_write_string(line)
        if ret is not None:
            write_string = ret
            continue
            
        ret = is_read_string(line)
        if ret is not None:
            read_string = ret
            if read_string != write_string:
                error_message = 'Error in line {}: \
                    String read "{}" is not equal to string written "{}"'\
                    .format(line_num+1, read_string, write_string)
                return False, error_message
            continue
    
    return True, None
