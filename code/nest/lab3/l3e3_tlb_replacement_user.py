import re
from collections import OrderedDict
from parse_result import *
from operator import attrgetter

def check(lines):
    exit_successfully = False
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
            rightCode = 148832
            if exitCode != rightCode:
                error_message = 'Error in line {}: \
                    The result of user program returned \
                    by syscall Exit() is wrong'\
                    .format(line_num+1)
                return False, error_message
            if exit_successfully is True:
                error_message = 'Error in line {}: \
                    Syscall Exit() is called more than 1 time'\
                    .format(line_num+1)
                return False, error_message
            exit_successfully = True
            continue
        
        ret = is_paging_summary(line)
        if ret is not None:
            fault_num = ret
            fifo_fault_num = 1216
            if fault_num < 1:
                error_message = 'Error in line {}: \
                    Paging fault num {} is less than 1'\
                    .format(line_num+1, fault_num)
                return False, error_message
            elif fault_num >= fifo_fault_num:
                error_message = 'Error in line {}: \
                    Your submitted tlb replacement algorithm should perform better than FIFO,\
                    whose page fault counts {}, and yours counts {}{}.'\
                    .format(line_num+1, fifo_fault_num, fault_num, \
                    ' too' if fault_num == fifo_fault_num else '')
                return False, error_message
            continue
    
    if exit_successfully is True:
        return True, 'Page fault count: {}'.format(fault_num)
    else:
        error_message = 'Error: syscall Exit() is not called or the debug message is modified'
        return False, error_message


