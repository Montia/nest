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
            if num not in num_tid:
                if tid in tid_num:
                    error_message = 'Error in line {} of the result: \
                        thread{} and thread{} have same tid {}\n'\
                        .format(line_num+1, tid_num[tid], num, tid)
                    return False, error_message
                num_tid[num] = tid
                tid_num[tid] = num
            else:
                if num_tid[num] != tid:
                    error_message = 'Error in line {} of the result: \
                        thread{} has different tid {} and {}\n'\
                        .format(line_num+1, num, num_tid[num], tid)
                    return False, error_message
    return True, None
