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

def is_getattr_false(line):
    a = re.findall(r"fileSystem->GetAttr\(\) returns FALSE.\n", line)
    if (len(a) > 0):
        return True
    else:
        return None

def is_write_string(line):
    a = re.findall("Write string (.*) to file\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_read_string(line):
    a = re.findall("Read string (.*) from file\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_getattr_true(line):
    a = re.findall(r"fileSystem->GetAttr\(\) succeeded, type: (.*), ctime: (.*), mtime: (.*), atime: (.*)\n", line)
    if (len(a) > 0):
        return (int(e) for e in a[0])
    else:
        return None

def check(lines):
    write_string = None
    success = False
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

        ret = is_getattr_false(line)
        if ret is not None:
            error_message = 'Error in line {}: \
                Getting attribute failed'\
                .format(line_num+1)
            return False, error_message

        ret = is_getattr_true(line)
        if ret is not None:
            file_type, ctime, mtime, atime = ret
            if file_type != 0:
                error_message = 'Error in line {}: \
                    File type is not 0 (FILE_TYPE_REG_FILE)'\
                    .format(line_num+1)
                return False, error_message
            if not ctime < mtime < atime:
                error_message = 'Error in line {}: \
                    The test created, writed, read the file with 2-second interval,\
                    so ctime({}) < mtime({}) < atime({}) is expected.'\
                    .format(line_num+1, ctime, mtime, atime)
                return False, error_message
            success = True
            continue
    if success:
        return True, None
    else:
        return False, "Not get attribute"
