import os
from os import listdir
from os.path import isfile, join
import shutil
from datetime import datetime

from file_read_backwards import FileReadBackwards

from condorgp.params import lean_dict, test_dict, util_dict

class Utils:
    def __init__(self):
        pass

    def cp_ind_to_lean_algos(self, file_path, filename):
        '''
        Copy a file to the
            lean_dict['LOCALPACKAGES_PATH']
        '''
        if filename[-3:] != '.py':
            filename = filename + '.py'
        src = file_path + filename
        dst = lean_dict['LOCALPACKAGES_PATH'] + filename
        shutil.copy(src, dst, follow_symlinks=True)

    def cp_config_to_lean_launcher(self, file_path, filename):
        '''
        Copy the file to
            lean_dict['LOCALPACKAGES_PATH']
        '''
        src_ingoing_config = file_path + filename
        dst_to_copy_to = lean_dict['LOCALPACKAGES_PATH'] + filename
        shutil.copy(src_ingoing_config, dst_to_copy_to, follow_symlinks=True)

    def delete_file_from_path(self, file_path, filename):
        '''
        delete file func
        '''
        file_to_delete = file_path + filename
        ## If file exists, delete it ##
        if os.path.isfile(file_to_delete):
            os.remove(file_to_delete)
        else:    ## Show an error ##
            print("Error: %s file not found" % file_to_delete)

    def check_recent_mod(self, input_file_paths):
        '''
        Returns true if all files in the path updated within
        'reasonable fitness seconds' set in params.py
        '''
        dt = datetime.now()
        now = datetime.timestamp(dt)
        diff = 1000*test_dict['REASONABLE_FITNESS_SECS']
        count = 0
        recent = 0
        onlyfiles = [f for f in listdir(input_file_paths) if isfile(join(input_file_paths, f))]
        for file_path in onlyfiles:
            count += 1
            if (now - os.path.getmtime(input_file_paths +'/'+ file_path)) < (now - diff): recent += 1
        if count == 0: return False
        if recent > 0: return True

    def pull_latest_log_into_overall_backtest_log(self):
        backtestfolder = test_dict['CONDORGP_IN_BACKTESTS_DIR']
        backtestlog = lean_dict['BACKTEST_LOG_LOCALPACKAGES']
        foundfolders = [f for f in listdir(backtestfolder) if not isfile(join(backtestfolder, f))]
        if len(foundfolders) > 0:
            latest = ''
            for folder in foundfolders:
                if folder > latest:
                    latest = folder
        if latest != '':
            # open file, and append to existing log
            latestlogs = self.get_all_lines(backtestfolder + latest + '/log.txt')
            # Open a file with access mode 'a'
            updatedlog = open(backtestlog, 'a')
            for line in latestlogs:
                updatedlog.write(line)
            updatedlog.close()
        return latest

    def cut_pys_from_latest_backtests_code_dir(self):
        latestfolder = test_dict['CONDORGP_IN_BACKTESTS_DIR'] + \
            self.pull_latest_log_into_overall_backtest_log() + '/code/'
        onlyfiles = \
            [f for f in listdir(latestfolder) if isfile(join(latestfolder, f))]
        for file in onlyfiles:
            os.rename(latestfolder+file, latestfolder+file[:-3])

    def get_all_lines(self, file_input):
        try:
            lines = open(file_input).readlines()
        except:
            print(f'ERROR opening this file: {file_input}')
            return []
        return lines

    def get_last_x_log_lines(self,
                lines = 150,
                log_file_n_path = lean_dict['BACKTEST_LOG_LOCALPACKAGES']):
        '''
        Get from the (default) log the last X lines
        '''
        list_lines = []
        count = 0
        with FileReadBackwards(log_file_n_path, encoding="utf-8") as frb:
            for l in frb:
                count += 1
                if count > lines: break
                # print(l)
                list_lines.append(l)
        return list_lines

    def confirm_ind_name_in_log_lines(self,output_ind):
        print(output_ind)
        results_list = self.get_last_x_log_lines(
                    lines =  util_dict['NO_LOG_LINES'],
                    log_file_n_path = lean_dict['BACKTEST_LOG_LOCALPACKAGES'])
        found_algo_name = False
        for line in results_list:
            if output_ind in line:
                print(line)
                found_algo_name = True
        return found_algo_name

    def retrieve_log_line_with_key(self,
            key,
            lines = 150,
            log_file_n_path = lean_dict['BACKTEST_LOG_LOCALPACKAGES']):
        '''
        Get the X lines of a log
        And search for the key given

        Returns a tuple:
            the FIRST line if found, or '' if not found
            the count of line number, given the no. lines

            N.B. First from the last X lines of the log...
                But taken in reverse order, last first as end of the log file
        '''
        log_to_search_list = self.get_last_x_log_lines(lines, log_file_n_path)
        # return both the line and it's index, to indicate where it was found
        for i, line in enumerate(log_to_search_list):
            if str(key) in line: return line, i
        return '', -1

    def get_keyed_line_in_limits(self,
            key,
            log_file_n_path = lean_dict['BACKTEST_LOG_LOCALPACKAGES'],
            limit_lines = util_dict['NO_LOG_LINES'],
            start_line = 0)-> tuple:
        '''
        TO DO: Return a tuple of:
            The retrived line in full that contains X
            Provided within the limit_lines after Z found
            How many lines after the start_line is found
        '''
        found_tuple = self.retrieve_log_line_with_key(
            key = key,
            log_file_n_path = log_file_n_path)

        line = found_tuple[0]
        no_lines_after_start = found_tuple[1]

        if line == '' and no_lines_after_start == -1:
            return 'not found', -1
        elif no_lines_after_start < start_line:
            return f'below limit given: {limit_lines}', -2
        elif no_lines_after_start > limit_lines:
            return f'past limit given: {limit_lines}', -3
        return line, no_lines_after_start

    def get_last_chars(self, line):
        temp = str.split(line,' ')
        return temp[-1]

    def get_fitness_from_log(self,
            key = lean_dict['FITNESS_CRITERIA'],
            log_file_n_path = lean_dict['BACKTEST_LOG_LOCALPACKAGES']):
        pass

    def overwrite_main_with_input_ind(self,input_ind):
        '''
        Replace main.py with our algorithm, from an existing .py file
        '''
        if input_ind[-3:] != '.py':
            input_ind = input_ind + '.py'
        self.cp_rename_algo_file_to_main(input_ind)
        self.rename_main_class_as_condorgp()

    def cp_rename_algo_file_to_main(self, input_ind):
        '''
        Rename file to main.py

        Requires our algo to be in the localpackages path
        '''
        f_path = lean_dict['LOCALPACKAGES_PATH']
        if input_ind[-3:] != '.py':
            input_ind = input_ind + '.py'
        src = f_path + input_ind
        dst = f_path + 'main.py'
        if src and dst:
            shutil.copy(src, dst, follow_symlinks=True)

    def cp_injected_algo_in_and_sort(self, base_algo_name_ext, injection_string):
        '''
        Take injected code, and inject. then copy across to
        localpackages, renamed file and class declaration.
        '''
        done_injectedAlgo_to_copy_in = lean_dict['LEAN_INJECTED_ALGO']

        # inject evolved code into algo py file
        self.inject_evolved_func_in(base_algo_name_ext, injection_string)

        # copy file across:
        self.copy_algo_in(done_injectedAlgo_to_copy_in)

        # rename 'gpInjectAlgo_done.py' to main.py
        self.cp_rename_algo_file_to_main('gpInjectAlgo_done.py')

        # go into gpInjectAlgo_done.py and rename class to condorgp:
        self.rename_main_class_as_condorgp(gpInjectAlgo_class_line = True)

    def inject_evolved_func_in(self, base_algo_name_ext, str_for_injection = ''):
        '''
        Inject the evolved function into the local:
            class gpInjectAlgo(QCAlgorithm)
        N.B.
        This then needs copying across into Local Packages, renaming etc
        '''
        config_path = lean_dict['CONDOR_CONFIG_PATH']
        f_name_n_path = config_path + lean_dict['LEAN_TO_INJECT_TEMPLATE_ALGO']
        f_name_n_path = f_name_n_path[0:-3] + base_algo_name_ext

        f_new_file = config_path + lean_dict['LEAN_INJECTED_ALGO']
        key_line = '## INJECT GP CODE HERE:'

        # careful here, the indentation is crucial,
        # see initial replacement line string:
        replacement_line = '''
    def newly_injected_code(self, data_in):
        self.Debug("eval_test_XX: injected_code_test {data_in}")'''
        if str_for_injection != '':
            replacement_line = str_for_injection

        with open(f_name_n_path, 'r') as f:
            lines = f.readlines()

        with open(f_new_file, 'w') as f:
            count = 0
            next = 0
            for line in lines:
                if key_line in line and count == 0:
                    count += 1
                if next == 1:
                    line = replacement_line
                    # print(line)
                if count > 0:
                    next += 1
                f.write(line)


    def rename_main_class_as_condorgp(self, gpInjectAlgo_class_line = False):
        '''
        Rename the class in the main.py to:
            class condorgp(QCAlgorithm)

        NB. Requires:
            1. file to be main.py
            2. in the Lean localpackages folder
        '''
        f_path = lean_dict['LOCALPACKAGES_PATH']
        key_line = 'class'
        replacement_line = "class condorgp(QCAlgorithm): \n"
        if gpInjectAlgo_class_line:
            replacement_line = "class gpInjectAlgo(QCAlgorithm): \n"

        main_py_for_class_rename = f_path + 'main.py'

        with open(main_py_for_class_rename, 'r') as f:
            lines = f.readlines()

        with open(main_py_for_class_rename, 'w') as f:
            count = 0
            for line in lines:
                if key_line in line and count == 0:
                    line = replacement_line
                    count += 1
                f.write(line)

    def delete_file_from_path(self, filepath, complete_filename):

        file_to_del = f'{filepath}{complete_filename}'

        if os.path.exists(file_to_del):
            os.remove(file_to_del)
        else:
            print(f"The file specified: {file_to_del} does not exist")

    def copy_config_in(self, input_ind):
        # copy config.json across before container launch
        if input_ind[-3:] == '.py':
            input_ind = input_ind[0:-3]
        if input_ind[-1] == '1':
            config_to_copy = test_dict['CONDOR_TEST_CONFIG_FILE_1']
        elif input_ind[-1] == '2':
            config_to_copy = test_dict['CONDOR_TEST_CONFIG_FILE_2']

        config_from_path = test_dict['CONDOR_CONFIG_PATH']
        self.cp_config_to_lean_launcher(config_from_path, config_to_copy)

    def copy_algo_in(self, input_ind):
        # copy algo.py across before container launch
        test_ind_path = lean_dict['CONDOR_CONFIG_PATH']
        self.cp_ind_to_lean_algos(test_ind_path, input_ind)
        self.overwrite_main_with_input_ind(input_ind)

    def list_pys_in_folder(self, folder):
        pys = []
        pys = [f for f in listdir(folder) if \
                isfile(join(folder, f)) and f[-3:] == '.py']
        return pys

    def del_pys_from_local_packages(self):
        test_algos_path = lean_dict['LOCALPACKAGES_PATH']
        pys = self.list_pys_in_folder(test_algos_path)
        if pys:
            for py in pys:
                self.delete_file_from_path(test_algos_path, py)

if __name__ == "__main__":
    pass
    print('going...')
    u = Utils()
    u.del_pys_from_local_packages()
    print(u.list_pys_in_folder(lean_dict['LOCALPACKAGES_PATH']))
#    u.cp_injected_algo_in_and_sort('_test_06.py','')


    # key_req = 'Return Over Maximum Drawdown'
    # limit_lines = 25 # util_dict['NO_LOG_LINES']
    # got = u.get_keyed_line_within_limits(key_req, limit_lines = limit_lines)

    # print(u.get_last_chars(got[0]))
    # print(type(u.get_last_chars(got[0])))


    # test_algos_path = lean_dict['LOCALPACKAGES_PATH']
    # input_ind = 'tester'
    # print(f"looking to delete:  {test_algos_path}{input_ind}.py")

    # u.delete_file_from_path(test_algos_path, input_ind+'.py')
    # assert not os.path.exists(f"{test_algos_path}{input_ind}.py")
