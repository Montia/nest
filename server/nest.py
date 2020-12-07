import os
import sys
import traceback

uploaded_root_dirname = 'nest_student'

def test_lab(lab, zipfile):
    # check if params are valid
    if type(lab) != int or lab < 1 or lab > 7:
        score = 0
        log = '<h4>Lab{} is invalid</h4>'.format(lab)
        return score, log.decode('utf-8')

    if type(zipfile) != str or not zipfile.endswith('.zip'):
        score = 0
        log = '<h4>Uploaded file {} is not a ".zip" file</h4>'.format(lab)
        return score, log.decode('utf-8')

    # make the directory for the uploaded code, where unzip inflates to 
    dest_dir = os.path.abspath(os.path.dirname(zipfile))
    inflated_dir = os.path.join(dest_dir, 'inflated')
    try:
        os.system('chmod -R 777 {}'.format(inflated_dir))
        os.system('rm -rf {}'.format(inflated_dir))
    except OSError:
        pass
    os.mkdir(inflated_dir)
    ret = os.system('unzip {} -d {} > {} 2>&1'.format(\
        zipfile, inflated_dir, os.path.join(dest_dir, 'unzip.result')))
    if ret != 0:
        score = 0
        log = '<h4>Unzip failed, ret = {}</h4>'.format(ret)
        log += 'Command unzip\'s output: <br/>'
        with open(os.path.join(dest_dir, 'unzip.result')) as f:
            for line in f.readlines():
                if line.startswith('note:'):
                    break
                log += line.replace('\n', '<br/>')
        return score, log.decode('utf-8')

    # check whether the uploaded code contains sole directory
    inflated_files = os.listdir(inflated_dir)
    if len(inflated_files) > 1 or inflated_files[0] != uploaded_root_dirname \
        or not os.path.isdir(os.path.join(inflated_dir, uploaded_root_dirname)):
        score = 0
        log = '<h4>The uploaded zip file should contain \
             only a directory named "nest". </h4>'
        log += 'Your zip file contain directory/files as follows: <br/>'
        for inflated_file in inflated_files:
            if os.path.isdir(os.path.join(inflated_dir, inflated_file)):
                file_type = 'directory'
            else:
                file_type = 'not directory'
            log += '{} ({}) <br/>'.format(inflated_file, file_type)

        return score, log.decode('utf-8')
    
    # check whether the code contains "code" directory
    uploaded_root_dir = os.path.join(inflated_dir, uploaded_root_dirname)
    code_dir = os.path.join(uploaded_root_dir, 'code')
    if not os.path.isdir(code_dir):
        score = 0
        log = '<h4>Your "{}" doesn\'t contain "code" directory. \
            </h4>'.format(uploaded_root_dirname)
        log += 'Your zip file contain directory/files as follows: <br/>'
        for inflated_file in inflated_files:
            if os.path.isdir(os.path.join(inflated_dir, inflated_file)):
                file_type = 'directory'
            else:
                file_type = 'not directory'
            log += '{} ({}) <br/>'.format(inflated_file, file_type)
        return score, log.decode('utf-8')

    # copy/overwrite directory "nest" and "machine"  
    nest_dir = os.path.join(code_dir, 'nest')
    try:
        os.system('chmod -R 777 {}'.format(nest_dir))
        os.system('rm -rf {}'.format(nest_dir))
    except OSError:
        pass
    os.system('cp -r code/nest {}'.format(code_dir))

    machine_dir = os.path.join(code_dir, 'machine')
    try:
        os.system('chmod -R 777 {}'.format(machine_dir))
        os.system('rm -rf {}'.format(machine_dir))
    except OSError:
        pass
    os.system('cp -r code/machine {}'.format(code_dir))

    # change directory to the given lab
    score = 0
    old_dir = os.getcwd()
    try:
        lab_dir = os.path.join(nest_dir, 'lab{}'.format(lab))
        os.chdir(lab_dir)
        
        # produce test results using Makefile
        os.system('make depend && make nest > {} 2>&1'\
            .format(os.path.join(dest_dir, 'make.result')))
        if ret != 0:
            score = 0
            log = '<h4>Make failed, ret = {}</h4>'.format(ret)
            log += 'Make\'s output: <br/>'
            with open(os.path.join(dest_dir, 'make.result')) as f:
                for line in f.readlines():
                    # if line.startswith('note:'):
                    #     break
                    log += line.replace('\n', '<br/>')
            return score, log.decode('utf-8')
        log = ''
        # log = 'lab{}: {}<br/>'.format(lab, os.getcwd())
        # for name in os.listdir('.'):
        #     log += '{} <br/>'.format(name)

        # parse and score the test results using scripts
        sys.path.append(os.getcwd())
        from score import tests
        # log += 'tests: {}<br/>'.format(tests)
        score = 0
        for test in tests:
            exec 'from {} import check'.format(test)
            # log += test+'.result\'s output is as follows:<br/>'
            with open(test+'.result') as f:
                lines = f.readlines()
            passed, error_message = check(lines)
            if passed is True:
                score += tests[test]
                log += '<br/>Test {} passed, score: {}.'.format(test, tests[test])

    except Exception as e:
        log = '<h4>Exception raised while testing.</h4>'
        exception_message = traceback.format_exc()
        log += exception_message.replace('\n', '<br/>')

    finally:
        try:
            sys.path.remove(os.getcwd())
        except ValueError as e:
            pass
        os.chdir(old_dir)
        # log += 'Change directory back to {} <br/>'.format(os.getcwd())

    return score, log.decode('utf-8')
