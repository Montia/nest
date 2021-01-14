import re
from collections import OrderedDict
from parse_result import *
from operator import attrgetter

def is_false_failure(line):
    a = re.findall('get_and_use_page\(\) returned (.*), but page (.*) is still unoccupied.\n', line)
    if (len(a) > 0):
        return int(a[0][1])
    else:
        return None

def is_page_too_large(line):
    a = re.findall('Page returned by get_and_use_page\(\) should be less than NumPhysPages(.*).\n', line)
    if (len(a) > 0):
        return True
    else:
        return None

def is_page_occupied(line):
    a = re.findall('get_and_use_page\(\) returned (.*), but it has been occupied.\n', line)
    if (len(a) > 0):
        return True
    else:
        return None

def check(lines):
    exit_successfully = False
    for line_num, line in enumerate(lines):
        ret = is_false_failure(line)
        if ret is not None:
            return False, 'Getting page failed, but there are pages unoccupied'
            
        ret = is_page_too_large(line)
        if ret is not None:
            return False, 'Page returned is not right'
            
        ret = is_page_occupied(line)
        if ret is not None:
            return False, 'Page returned has been occupied'
    
    return True, None


