import pytest
from aspr.sim.state import State, StateStatistics
from aspr.sim.interference_model import BinaryInterference

def test_copy_01():
  state = State().init(size=5, int_model=BinaryInterference(), colors=range(5))
  state.tick().activate(0)
  copy_state = state.copy()
  copy_state.tick().activate(1)

  assert copy_state.count_active_nodes() != state.count_active_nodes()
  assert copy_state.t != state.t
  assert copy_state.actvn_cnt != state.actvn_cnt


def test_copy_02():
  state = State().init(size=5, int_model=BinaryInterference(), colors=range(5))
  state.tick().activate(0)
  copy_state = state.copy()

  assert copy_state.count_active_nodes() == state.count_active_nodes()
  assert copy_state.t == state.t
  assert copy_state.actvn_cnt == state.actvn_cnt


def test_score_01():
  pass


def test_count_active_nodes_01():
  state = State().init(size=5, int_model=BinaryInterference(), colors=range(5))
  state.tick().activate(0)
  assert state.count_active_nodes() == 1


def test_count_active_nodes_02():
  state = State().init(size=5, int_model=BinaryInterference(), colors=range(5))
  state.tick().activate(0)._tick(8).activate(1)._tick(8)
  assert state.count_active_nodes() == 1


def test_count_active_nodes_03():
  state = State().init(size=5, int_model=BinaryInterference(), colors=range(5))
  state.tick().activate(0).tick().activate(1)
  assert state.count_active_nodes() == 2


def test_count_active_nodes_04():
  state = State().init(size=5, int_model=BinaryInterference(), colors=range(5))
  state.tick().activate(0)._tick(12)
  assert state.count_active_nodes() == 0


def test_all_nodes_expired_01():
  state = State().init(size=2, int_model=BinaryInterference(), colors=range(5))
  state.tick().\
        activate(0).\
        tick().\
        activate(1).\
        _tick(12)
  assert state.all_nodes_expired() == True


def test_all_nodes_expired_02():
  state = State().init(size=2, int_model=BinaryInterference(), colors=range(5))
  state.tick().\
        activate(0).\
        tick().\
        activate(1).\
        _tick(5)
  assert state.all_nodes_expired() == False


def test_active_per_color_01():
  state = State().init(size = 5, int_model=BinaryInterference(), colors=range(5))
  state.tick().\
        activate(0).\
        tick().\
        activate(1).\
        tick().\
        activate(0).\
        tick()
  stats = StateStatistics(state)
  assert stats.active_per_color() == {
    'c0-n-active': 2, 
    'c1-n-active': 1, 
    'c2-n-active': 0, 
    'c3-n-active': 0 , 
    'c4-n-active': 0}


def test_active_per_color_02():
  state = State().init(size = 5, int_model=BinaryInterference(), colors=range(5))
  state.tick().\
        activate(0).\
        _tick(5).\
        activate(3).\
        tick().\
        activate(0).\
        _tick(5)
  stats = StateStatistics(state)
  assert stats.active_per_color() == {
  'c0-n-active': 1, 
  'c1-n-active': 0, 
  'c2-n-active': 0, 
  'c3-n-active': 1, 
  'c4-n-active': 0}


def test_ttl_per_color_01():
  state = State().init(size = 5, int_model=BinaryInterference(), colors=range(5))
  state.tick().\
        activate(0).\
        tick().\
        activate(1).\
        tick().\
        activate(0).\
        tick()
  stats = StateStatistics(state)
  assert stats.ttl_per_color() == {
  'c0-total-ttl': 16, 
  'c1-total-ttl': 8, 
  'c2-total-ttl': 0, 
  'c3-total-ttl': 0, 
  'c4-total-ttl': 0}


def test_ttl_per_color_02():
  state = State().init(size = 5, int_model=BinaryInterference(), colors=range(5))
  state.tick().\
        activate(0).\
        _tick(5).\
        activate(3).\
        tick().\
        activate(0).\
        _tick(5)
  stats = StateStatistics(state)
  assert stats.ttl_per_color() == {
  'c0-total-ttl': 5, 
  'c1-total-ttl': 0, 
  'c2-total-ttl': 0, 
  'c3-total-ttl': 4, 
  'c4-total-ttl': 0}
