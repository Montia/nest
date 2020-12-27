import re

def is_print_tid(line):
    a = re.findall('\*\*\* thread (.*)\'s tid is (.*) \*\*\*\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def check(lines):
    num_tid = {}
    tid_num = {}
    for line_num, line in enumerate(lines):
        ret = is_print_tid(line)
        if ret is not None:
            num, tid = ret
            num = int(num)
            tid = int(tid)
            if tid < 0:
                error_message = 'Error in line {}: \
                    thread{}\'s tid is {}, which should be positive.\n'\
                    .format(line_num+1, num, tid)
                return False, error_message
            
            if num not in num_tid:
                if tid in tid_num:
                    error_message = 'Error in line {}: \
                        thread{} and thread{} have same tid {}\n'\
                        .format(line_num+1, tid_num[tid], num, tid)
                    return False, error_message
                num_tid[num] = tid
                tid_num[tid] = num
            else:
                if num_tid[num] != tid:
                    error_message = 'Error in line {}: \
                        thread{} has different tid {} and {}\n'\
                        .format(line_num+1, num, num_tid[num], tid)
                    return False, error_message
    if len(num_tid) < 2:
        return False, 'There should be at least 2 threads launched, {} actually.'.format(len(num_tid))
    return True, None
