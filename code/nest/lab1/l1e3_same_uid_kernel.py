import re

def is_print_tid(line):
    a = re.findall('\*\*\* thread (.*)\'s uid is (.*) \*\*\*\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def check(lines):
    sole_uid = None
    for line_num, line in enumerate(lines):
        ret = is_print_tid(line)
        if ret is not None:
            num, uid = ret
            num = int(num)
            uid = int(uid)
            if uid < 0:
                error_message = 'Error in line {}: \
                    thread{}\'s uid is {}, which should be positive.\n'\
                    .format(line_num+1, num, uid)
                return False, error_message
            
            if sole_uid is None:
                sole_uid = uid
            elif uid != sole_uid:
                error_message = 'Error in line {}: \
                    thread{}\'s uid is {}, but other thread has uid {}.\n'\
                    .format(line_num+1, num, uid, sole_uid)
                return False, error_message
    return True, None
