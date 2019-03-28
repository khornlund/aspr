import pytest

from aspr.sim.scenario import Scenario
from aspr.sim.decision_model import RoundRobinDecision
from aspr.sim.interference_model import BinaryInterference


@pytest.fixture()
def rr_dec_model():
    return RoundRobinDecision(colors=[0, 1])


@pytest.fixture()
def binary_int_model():
    return BinaryInterference()


def test_spawn_time_01(rr_dec_model, binary_int_model):
    scenario = Scenario(
        n_nodes=2,
        spt=[1, 2],
        colors=range(5),
        dec_model=rr_dec_model,
        int_model=binary_int_model,
        name='test_spawn_time_01')

    scenario.run()
    df = scenario.to_df()

    # test spawns occur correctly
    assert df.loc[1, 'n0-color'] == 0
    assert df.loc[1, 'n1-color'] == -1
    assert df.loc[2, 'n1-color'] == 1


def test_ttl_expire_01(rr_dec_model, binary_int_model):
    scenario = Scenario(
        n_nodes=2,
        spt=[1, 2],
        colors=range(5),
        dec_model=rr_dec_model,
        int_model=binary_int_model,
        name='test_ttl_expire_01')

    scenario.run()
    df = scenario.to_df()

    # test ttl expires correctly
    assert df.loc[10, 'n0-ttl'] == 1
    assert df.loc[11, 'n0-ttl'] == 0
    assert df.loc[11, 'n1-ttl'] == 1
    assert df.loc[12, 'n1-ttl'] == 0


def test_color_reset_01(rr_dec_model, binary_int_model):
    scenario = Scenario(
        n_nodes=2,
        spt=[1, 2],
        colors=range(5),
        dec_model=rr_dec_model,
        int_model=binary_int_model,
        name='test_color_reset_01')

    scenario.run()
    df = scenario.to_df()

    # test color reset correctly
    assert df.loc[11, 'n0-color'] == 0
    assert df.loc[12, 'n0-color'] == -1
    assert df.loc[12, 'n1-color'] == 1
    assert df.loc[13, 'n1-color'] == -1
