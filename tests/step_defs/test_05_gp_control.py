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

scenarios('../features/05_gp_control.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean tests each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
  Scenario Outline: GpControl can set different psets as needed
    Given a specific pair of psets needed
    When GpControl receieves a requirement for a "<pset_input>"
    And a Deap run is conducted
    Then the pset returned is not the same as the base_pset

    Examples:
      | pset_input      |
      | psetA           |
      | psetB           |
"""

# 'Successfully ran '.' in the 'backtesting' environment and stored the output in'

@given('a setup with Deap using Lean')
def setup_ready():
    pass # assumes, rest of test to prove

@when(parsers.cfparse('Deap specs Lean to run "{input_ind:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='input_ind')
@when('Deap specs Lean to run "<input_ind>"', target_fixture='input_ind')
def deap_sets_algo_to_Lean(utils, input_ind):
    ''' copies across config files and algorithms as needed '''
    utils.copy_config_in(input_ind)
    utils.copy_algo_in(input_ind)

@when('a short Deap run is conducted')
def short_deap_run(deap_one):
    assert deap_one is not None
    newpop = 1
    deap_one.setup_gp()
    deap_one.set_population(newpop)
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
