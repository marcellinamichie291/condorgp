from condorgp.util.utils import Utils
from condorgp.gp.gp_deap import GpDeap
from condorgp.gp.gp_psets import GpPsets
from condorgp.evaluation.lean_runner import RunLean
from condorgp.util.log import CondorLogger

class InitialFactory:
    def __init__(self):
        pass

    def get_utils(self):
        return Utils()

    def get_gp_provider(self):
        return GpDeap()

    def get_gp_psets(self, customfuncs):
        return GpPsets(customfuncs)

    def get_lean_runner(self):
        return RunLean()

    def get_logger(self):
        return CondorLogger().get_logger()
