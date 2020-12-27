import re

def false_fork_fail(line):
    a = re.findall('Forking (.*) failed!\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def false_fork_success(line):
    a = re.findall('Forking (.*) succeeded, but over limit\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def check(lines):
    for line_num, line in enumerate(lines):
        thread_name = false_fork_fail(line)
        if thread_name is not None:
            error_message = 'Error in line {}: Forking {} failed.\n'\
                .format(line_num+1, thread_name)
            return False, error_message
        thread_name = false_fork_success(line)
        if thread_name is not None:
            error_message = 'Error in line {}: \
                Forking {} succeeded, but over thread limit\
                (thread \"main\" should also be counted).\n'\
                .format(line_num+1, thread_name)
            return False, error_message
    return True, None
