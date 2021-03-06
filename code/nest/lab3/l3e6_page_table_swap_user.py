import re
from collections import OrderedDict
from parse_result import *
from operator import attrgetter

def check(lines):
    exit_successfully = 0
    for line_num, line in enumerate(lines):
        ret = is_unexpected_exception(line)
        if ret is not None:
            which, type_ = ret
            if which == 2:
                error_message = 'Error in line {}: \
                    Page fault handler is not implemented'\
                    .format(line_num+1)
                return False, error_message
            if which == 1 and type_ == 1:
                error_message = 'Error in line {}: \
                    Syscall Exit() is not implemented'\
                    .format(line_num+1)
                return False, error_message
            error_message = 'Error in line {}: \
                Unexpected user mode exception {} {}'\
                .format(line_num+1, which, type_)
            return False, error_message

        ret = is_user_program_exit(line)
        if ret is not None:
            exitCode = ret
            rightCode = sum(i*i for i in range(128))
            if exitCode != rightCode:
                error_message = 'Error in line {}: \
                    The result of user program returned \
                    by syscall Exit() is wrong'\
                    .format(line_num+1)
                return False, error_message
            exit_successfully += 1
            continue
    
    if exit_successfully == 2:
        return True, None
    else:
        error_message = 'Error: there are 2 user processes, but syscall Exit() called {} times'.format(exit_successfully)
        return False, error_message


