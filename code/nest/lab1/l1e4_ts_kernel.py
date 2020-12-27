import re
from collections import namedtuple
from collections import OrderedDict
# import sys
# raise Exception(str(sys.path))
from parse_result import *

def is_ts_call(line):
    a = re.findall('Call ts\(\) from thread (.*)\n', line)
    if (len(a) > 0):
        return a[0]
    else:
        return None

def check(lines):
    class ThreadInfo:
        def __init__(self, name=None, status=None, tid=None, uid=None):
            self.tid = tid
            self.uid = uid
            self.name = name
            self.status = status
        
        def __eq__(self, other):
            if self.tid is None:
                self.tid = other.tid
                self.uid = other.uid
            elif other.tid is None:
                other.tid = self.tid
                other.uid = self.uid
            return self.uid == other.uid and self.tid == other.tid \
                and self.name == other.name and self.status == other.status
        
        def __str__(self):
            return 'Thread(name={!s}, status={!s}, tid={!s}, uid={!s})'\
                .format(self.name, self.status, self.tid, self.uid)
        
        def __repr__(self):
            return 'Thread(name={!s}, status={!s}, tid={!s}, uid={!s})'\
                .format(self.name, self.status, self.tid, self.uid)

    current_threads = OrderedDict()
    current_threads.setdefault('main', ThreadInfo('main')).status = 'Running'
    in_ts = False
    for line_num, line in enumerate(lines):
        if not in_ts:
            ret = is_ts_call(line)
            if ret is not None:
                in_ts = True
                continue
            
            ret = is_put_thread_on_ready_list(line)
            if ret is not None:
                name = ret
                current_threads.setdefault(name, ThreadInfo(name)).status = 'Ready'
                continue
            
            ret = is_switch_thread(line)
            if ret is not None:
                name = ret[1]
                if name not in current_threads:
                    error_message = 'Error in line {}: \
                        Unknown thread {} is Running'\
                        .format(line_num+1, name)
                    return False, error_message
                current_threads[name].status = 'Running'
                continue
            
            ret = is_sleep_thread(line)
            if ret is not None:
                name = ret
                if name not in current_threads:
                    error_message = 'Error in line {}: \
                        Unknown thread {} is Blocked'\
                        .format(line_num+1, name)
                    return False, error_message
                current_threads[name].status = 'Blocked'
                continue
            
            ret = is_delete_thread(line)
            if ret is not None:
                name = ret
                if name not in current_threads:
                    error_message = 'Error in line {}: \
                        Unknown thread {} is deleted'\
                        .format(line_num+1, name)
                    return False, error_message
                del current_threads[name]
                continue
        else:
            if line == '\n':
                in_ts = False
                if ts != current_threads:
                    return False, 'ts() should return {},<br/> but yours returns {}'.format(current_threads.values(), ts.values())
                continue
            
            ret = re.findall('(.*)\t(.*)\t(.*)\t(.*)\n', line)
            if len(ret) == 0:
                return False, 'You can only use original ts_print() to print in ts(), no other debug messages'
            tid, uid, name, status = ret[0]
            if tid == 'TID':
                ts = OrderedDict()
            else:
                ts[name] = ThreadInfo(name, status, int(tid), int(uid))
    
    return True, None
