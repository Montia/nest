import re
from collections import namedtuple
from collections import OrderedDict
from operator import attrgetter
# import sys
# raise Exception(str(sys.path))
from parse_result import *

def is_create_false(line):
    a = re.findall(r"fileSystem->Create\((.*)\) returns FALSE.\n", line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def is_mkdir_false(line):
    a = re.findall(r"fileSystem->Create\((.*)\) returns FALSE.\n", line)
    if (len(a) > 0):
        return a[0]
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
    a = re.findall(r"fileSystem->GetAttr\((.*)\) succeeded, type: (.*), ctime: (.*), mtime: (.*), atime: (.*)\n", line)
    if (len(a) > 0):
        return (a[0][0],) + tuple(int(e) for e in a[0][1:])
    else:
        return None

def directory_valid(name):
    return all(a.startswith('dir') or a == '' for a in name.split('/')[:-1])

def check(lines):
    write_string = None
    type_enum = {0:'file', 1:'dir'}
    success = 0
    failure = 0
    for line_num, line in enumerate(lines):
        ret = is_create_false(line)
        if ret is not None:
            name = ret
            if directory_valid(name):
                error_message = 'Error in line {}: \
                    Creating file {} failed'\
                    .format(line_num+1, name)
                return False, error_message
            else:
                failure += 1

        ret = is_mkdir_false(line)
        if ret is not None:
            name = ret
            if directory_valid(name):
                error_message = 'Error in line {}: \
                    Creating directory {} failed'\
                    .format(line_num+1, name)
                return False, error_message
            else:
                failure += 1

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
            name, file_type, ctime, mtime, atime = ret
            if not directory_valid(name):
                error_message = 'Error in line {}: \
                    {}\'s directory is not valid, but created successfully'\
                    .format(line_num+1, name)
                return False, error_message
            if not name.split('/')[-1].startswith(type_enum[file_type]):
                error_message = 'Error in line {}: \
                    File type {} is not correct for file {}'\
                    .format(line_num+1, file_type, name)
                return False, error_message
            success += 1
            continue
    
    if success == 6 and failure == 4:
        return True, None
    else:
        return False, '6 GetAttr, 4 failure not all succeeded'
