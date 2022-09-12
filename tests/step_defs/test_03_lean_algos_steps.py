import os

from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.utils import get_last_x_log_lines
from condorgp.utils import cp_config_to_lean_launcher
from condorgp.utils import cp_ind_to_lean_algos
from condorgp.utils import overwrite_main_with_input_ind

from condorgp.params import lean_dict, test_dict, util_dict

from condorgp.lean_runner import RunLean

EXTRA_TYPES = {
    'Number': int,
    'String': str,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../features/03_lean_algos.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean tests each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Scenario Outline: Lean tests each individual
    Given a Lean container ready to run
    And an evolved "<individual>" is specified
    When Lean runs the "<input_ind>" via the CLI
    Then the "<individual>" is used
    And the "<input_ind>" algorithm is tidied away
"""

# LEAN_ALGOS_FOLDER
# copy_ind_to_lean_algos_dir

@given('a Lean container ready to run')
def lean_container_tested_already():
    pass # assumes local lean:latest image extant

@given(parsers.cfparse('an evolved "{input_ind:String}" is specified',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@given('an evolved "<input_ind>" is specified', target_fixture='input_ind')
def copy_config_n_algo_across(input_ind):
    '''
    copies across config files and algorithms as needed
    '''
    copy_config_in(input_ind)
    copy_algo_in(input_ind)

def copy_config_in(input_ind):
    # copy config.json across before container launch
    config_from_path = test_dict['CONDOR_CONFIG_PATH']
    if input_ind[-1] == '1':
        config_to_copy = test_dict['CONDOR_TEST_CONFIG_FILE_1']
    elif input_ind[-1] == '2':
        config_to_copy = test_dict['CONDOR_TEST_CONFIG_FILE_2']
    cp_config_to_lean_launcher(config_from_path, config_to_copy)
    overwrite_main_with_input_ind(input_ind + '.py')

def     copy_algo_in(input_ind):
    # copy algo.py across before container launch
    test_ind_path = test_dict['CONDOR_TEST_ALGOS_FOLDER']
    cp_ind_to_lean_algos(test_ind_path, input_ind + '.py')

@when(parsers.cfparse('Lean runs the "{input_ind:String}" via the CLI',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@when('Lean runs the "<input_ind>" via the CLI', target_fixture='input_ind')
def set_lean_runner(input_ind):
    '''uses the utils method to set an os system command via Lean CLI'''
    # TO DO: not DRY!
    config_to_run = ''
    if input_ind[-1] == '1':
        config_to_run = test_dict['CONFIG_TEST_ALGOS_FILE_1']
    elif input_ind[-1] == '2':
        config_to_run = test_dict['CONFIG_TEST_ALGOS_FILE_2']
    lean = RunLean()
    lean.run_lean_via_CLI(input_ind, config_to_run)

@then(parsers.cfparse('the "{output_ind:String}" is found',
                       extra_types=EXTRA_TYPES), target_fixture='output_ind')
@then('the "<output_ind>" is found', target_fixture='output_ind')
def results_files_are_updated(output_ind):
    '''
    checks in the log file that the algo name is found
    only uses the last 150 lines of the log file
    '''
    print(output_ind)
    no_lines = util_dict['NO_LOG_LINES']
    results_list = get_last_x_log_lines(
                            lines = no_lines,
                            log_file_n_path = lean_dict['BACKTEST_LOG_LOCALPACKAGES'])
    found_algo_name = False
    for line in results_list:
        if output_ind in line:
            print(line)
            found_algo_name = True
    assert found_algo_name

@then(parsers.cfparse('the "{input_ind:String}" algorithm is tidied away',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@then('the "<input_ind>" algorithm is tidied away')
def tidy_up_algorithms(input_ind):
    '''
    deletes on algorithms
    '''
    test_algos_path = lean_dict['LEAN_ALGOS_FOLDER']
    # delete_file_from_path(test_algos_path, input_ind+'.py')
