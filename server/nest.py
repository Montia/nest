import os
import sys
import traceback

uploaded_root_dirname = 'nest_student'

def test_lab(lab, zipfile):
    # check if params are valid
    if type(lab) != int or lab < 1 or lab > 7:
        score = 0
        test_result = '<h4>Lab{} is invalid</h4>'.format(lab)
        return score, test_result.decode('utf-8')

    if type(zipfile) != str or not zipfile.endswith('.zip'):
        score = 0
        test_result = '<h4>Uploaded file {} is not a ".zip" file</h4>'.format(lab)
        return score, test_result.decode('utf-8')

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
        zipfile, inflated_dir, os.path.join(dest_dir, 'unzip.output')))
    if ret != 0:
        score = 0
        test_result = '<h4>Unzip failed, ret = {}</h4>'.format(ret)
        test_result += 'Command unzip\'s output: <br/>'
        with open(os.path.join(dest_dir, 'unzip.output')) as f:
            for line in f.readlines():
                if line.startswith('note:'):
                    break
                test_result += line.replace('\n', '<br/>')
        return score, test_result.decode('utf-8')

    # check whether the uploaded code contains sole directory
    inflated_files = os.listdir(inflated_dir)
    if len(inflated_files) > 1 or inflated_files[0] != uploaded_root_dirname \
        or not os.path.isdir(os.path.join(inflated_dir, uploaded_root_dirname)):
        score = 0
        test_result = '<h4>The uploaded zip file should contain \
             only a directory named "nest". </h4>'
        test_result += 'Your zip file contain directory/files as follows: <br/>'
        for inflated_file in inflated_files:
            if os.path.isdir(os.path.join(inflated_dir, inflated_file)):
                file_type = 'directory'
            else:
                file_type = 'not directory'
            test_result += '{} ({}) <br/>'.format(inflated_file, file_type)

        return score, test_result.decode('utf-8')
    
    # check whether the code contains "code" directory
    uploaded_root_dir = os.path.join(inflated_dir, uploaded_root_dirname)
    code_dir = os.path.join(uploaded_root_dir, 'code')
    if not os.path.isdir(code_dir):
        score = 0
        test_result = '<h4>Your "{}" doesn\'t contain "code" directory. \
            </h4>'.format(uploaded_root_dirname)
        test_result += 'Your zip file contain directory/files as follows: <br/>'
        for inflated_file in inflated_files:
            if os.path.isdir(os.path.join(inflated_dir, inflated_file)):
                file_type = 'directory'
            else:
                file_type = 'not directory'
            test_result += '{} ({}) <br/>'.format(inflated_file, file_type)
        return score, test_result.decode('utf-8')

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
        
        # parse and score the test results using scripts
        sys.path.append(os.getcwd())
        sys.path.append(os.getcwd()+'/..')
        from score import tests

        # produce test results using Makefile
        if lab == 2:
            for test in tests:
                makefile_name = 'Makefile.{}'.format(test)
                ret = os.system('make -f {0} clean && make -f {0} nest > {1} 2>&1'\
                    .format(makefile_name, 'make_nest.result'))
                if ret != 0:
                    score = 0
                    test_result = '<h4>Make failed, ret = {}</h4>'.format(ret)
                    test_result += 'Make\'s output: <br/>'
                    with open('make_nest.result') as f:
                        for line in f.readlines():
                            # if line.startswith('note:'):
                            #     break
                            test_result += line.replace('\n', '<br/>')
                    return score, test_result.decode('utf-8')
        else:
            ret = os.system('make depend > {} 2>&1'\
                .format(os.path.join(dest_dir, 'make_depend.result')))
            if ret != 0:
                score = 0
                test_result = '<h4>Make depend failed, ret = {}</h4>'.format(ret)
                test_result += 'Make\'s output: <br/>'
                with open(os.path.join(dest_dir, 'make_depend.result')) as f:
                    for line in f.readlines():
                        # if line.startswith('note:'):
                        #     break
                        test_result += line.replace('\n', '<br/>')
                return score, test_result.decode('utf-8')
            # produce test results using Makefile
            ret = os.system('make nest > {} 2>&1'\
                .format(os.path.join(dest_dir, 'make_nest.result')))
            if ret != 0:
                score = 0
                test_result = '<h4>Make failed, ret = {}</h4>'.format(ret)
                test_result += 'Make\'s output: <br/>'
                with open(os.path.join(dest_dir, 'make_nest.result')) as f:
                    for line in f.readlines():
                        # if line.startswith('note:'):
                        #     break
                        test_result += line.replace('\n', '<br/>')
                return score, test_result.decode('utf-8')
        
        test_result = ''
        score = 0
        for test in tests:
            if test.endswith('kernel'):
                ret = os.system('./nachos_test_{0} -d > {0}.result 2>&1'.format(test))
            elif test.endswith('user'):
                ret = os.system('./nachos_test_{0} -d -x {0}.noff > {0}.result 2>&1'.format(test))
            else:
                test_result += '<b>Test {} failed.<br/>{}<br/></b>'.format(test, 'Only support cases ending with"kernel" and "user"')
                test_result += '<br/>'
                continue
            if ret != 0:
                test_result += '<b>Test {} failed.<br/>{}<br/></b>'.format(test, 'Runtime Error')
                test_result += open(test+'.result').read().replace('\n', '<br/>')
                test_result += '<br/>'
                continue

            exec 'from {} import check'.format(test)
            # test_result += test+'.result\'s output is as follows:<br/>'
            with open(test+'.result') as f:
                lines = f.readlines()
            passed, error_message = check(lines)
            if passed is True:
                score += tests[test]
                test_result += '<b>Test {} passed, score: {}.<br/></b>'.format(test, tests[test])
            else:
                error_message = error_message.strip('\n')
                test_result += '<b>Test {} failed.<br/>{}<br/></b>'.format(test, error_message)
                with open(test+'.result') as f:
                    for line_num, line in enumerate(f.readlines()):
                        test_result += '{}\t{}'.format(line_num+1, line).replace('\n', '<br/>')
                test_result += '<br/>'

    except Exception as e:
        test_result = '<h4>Exception raised while testing.</h4>'
        exception_message = traceback.format_exc()
        test_result += exception_message.replace('\n', '<br/>')

    finally:
        if os.getcwd() != old_dir:
            try:
                sys.path.remove(os.getcwd())
                sys.path.remove(os.getcwd()+'/..')
            except ValueError as e:
                pass
            os.chdir(old_dir)

    return score, test_result.decode('utf-8', "replace")
