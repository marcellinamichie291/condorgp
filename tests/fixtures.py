import pytest
from condorgp.util.utils import Utils
from condorgp.gp.gp_control import GpControl
from condorgp.learning.dependency_factory import DependencyFactory
from condorgp.learning.dependency_factory_overridden import DependencyFactoryOverridden

@pytest.fixture
def utils():
    return Utils()

@pytest.fixture
def deap_one(): # this needs to be updated in tests numbered < 5
    return GpControl()

@pytest.fixture
def gpc():
    return GpControl()

@pytest.fixture
def gpc2():
    return GpControl()

@pytest.fixture
def gpc3():
    return GpControl()

@pytest.fixture
def dep_di():
    return DependencyFactory().get_dependency()

@pytest.fixture
def dep_di_mock():
    return DependencyFactoryOverridden().get_dependency()
