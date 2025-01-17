import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from tests.fixtures import deap_one, utils
from condorgp.params import lean_dict, test_dict, util_dict
from condorgp.evaluation.lean_runner import RunLean

EXTRA_TYPES = {
    'Number': int,
    'String': str,
    'Float': float,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../../features/04_deap_runs_lean.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean tests each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
  Scenario Outline: Lean is run and reports success and fitness
    Given a setup with Deap using Lean
    When Deap specs Lean to run "<input_ind>"
    And a short Deap run is conducted
    Then the result: "<ROI_over_MDD_value>" is found
    And the "<input_ind>" algorithm is tidied away

    Examples:
      | input_ind       |   output_ind       |   ROI_over_MDD_value    |
      | IndBasicAlgo1   |   IndBasicAlgo1    |   74.891                |
"""

# 'Successfully ran '.' in the 'backtesting' environment and stored the output in'

@given('a setup with Deap using Lean')
def setup_ready():
    pass # assumes, rest of test to prove

@when(parsers.cfparse('Deap specs Lean to run "{input_ind:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='input_ind')
@when('Deap specs Lean to run "<input_ind>"', target_fixture='input_ind')
@pytest.mark.usefixtures("utils")
def deap_sets_algo_to_Lean(utils, input_ind):
    ''' copies across config files and algorithms as needed '''
    utils.copy_config_in(input_ind)
    utils.copy_algo_in(input_ind)

@when('a short Deap run is conducted')
@pytest.mark.usefixtures("gpc")
def short_deap_run(deap_one):
    assert deap_one is not None
    newpop = 1
    gens = 1
    deap_one.setup_gp('', newpop, gens)
    deap_one.run_gp()

@then(parsers.cfparse('the result: "{ROI_over_MDD_value:Float}" is found',
                       extra_types=EXTRA_TYPES), target_fixture='ROI_over_MDD_value')
@then('the result: "<ROI_over_MDD_value>" is found')
def find_results(ROI_over_MDD_value, deap_one):
    max_fitness_found = deap_one.gp.logbook.select("max")[-1]
    assert ROI_over_MDD_value >= max_fitness_found

@then(parsers.cfparse('the "{input_ind:String}" algorithm is tidied away',
                        extra_types=EXTRA_TYPES),
                        target_fixture='input_ind')
@then('the "<input_ind>" algorithm is tidied away')
def output_ind_found(utils, input_ind):
    ''' deletes algorithms on path as found.'''
    test_algos_path = lean_dict['LOCALPACKAGES_PATH']
    utils.delete_file_from_path(test_algos_path, input_ind+'.py')
    assert not os.path.exists(f"{test_algos_path}{input_ind}.py")
