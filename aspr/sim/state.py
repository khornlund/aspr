import pandas as pd
import numpy as np
import copy
from aspr.sim.utils import _setup_logger
from aspr.sim.node import Node

class State:
  """Encapsulates the state of a scenario at a given point in time.

  Note: use .init() to initialise with values.

  Parameters
  ----------

  size (int) : the number of nodes

  int_model (InterferenceModel) : the model to use to calculate intereference
  between nodes

  colors (list(int)) : the available colors for node activation

  verbose (int) : Log level.
  """
  @property
  def name(self): return self.__class__.__name__

  def init(self, size, int_model, colors, verbose=0):
    """Non-ctor method to init so blank instances can be created for .copy()"""
    self.t = 0
    self.int_model = int_model
    self.colors = colors
    self.actvn_cnt = 0
    self.nodes = []
    for i in range(size):
      self.nodes.append(Node(i))
    self.logger = _setup_logger(self, verbose=verbose)
    return self


  def _copy(self, target):
    #TODO: is there a better way of doing this?
    self.t = target.t
    self.int_model = copy.deepcopy(target.int_model)
    self.actvn_cnt = copy.deepcopy(target.actvn_cnt)
    self.nodes  = copy.deepcopy(target.nodes)
    self.colors = copy.deepcopy(target.colors)
    self.logger = target.logger
    return self


  def copy(self):
    return State()._copy(self)


  def tick(self):
    self.logger.debug('tick: ..')
    self.t += 1
    for n in self.nodes:
      n.tick()
    return self


  def _tick(self, n):
    """Useful for testing"""
    for _ in range(n): self.tick()
    return self


  def activate(self, color):
    if self.actvn_cnt >= len(self.nodes):
      self.logger.debug('All nodes already activated. Continuing.')
      return
    self.logger.debug(f'Activating: n{self.actvn_cnt} <- c{color}')
    self.nodes[self.actvn_cnt].color = color
    self.actvn_cnt += 1
    return self


  def score(self):
    sum = 0
    for u in self.nodes:
      for v in self.nodes:
        if u.id != v.id:
          sum += self.int_model.calc(u, v)
    return sum/2


  def to_dict(self):
    d = {'t': self.t}
    for n in self.nodes: d.update(n.to_dict())
    d['score'] = self.score()
    stats = StateStatistics(self)
    d.update(stats.active_per_color())
    d.update(stats.ttl_per_color())
    return d


  def count_active_nodes(self):
    return [n.color != -1 for n in self.nodes].count(True)


  def all_nodes_expired(self):
    return all([n.ttl <= 0 for n in self.nodes])


class StateStatistics():
  """Computes statistics from a State object"""
  def __init__(self, state):
    self.state = state
    self.colors = state.colors


  def active_per_color(self):
    active_colors = [n.color for n in self.state.nodes]
    d = {f'c{c}-n-active': active_colors.count(c) for c in self.colors}
    return d


  def ttl_per_color(self):
    node_d = {c: [n for n in self.state.nodes if n.color == c] 
      for c in self.colors}
    ttl_d = {f'c{c}-total-ttl': sum([n.ttl for n in nodes]) for c, nodes in node_d.items()}
    return ttl_d


  def total_activated(self):
    pass


class History:
  """Stores a list of State objects"""

  def __init__(self, initial_state):
    self._records = [initial_state.copy()]


  def record(self, state):
    self._records.append(state.copy())


  def read(self, i = None):
    if i != None: return self._records[i].copy()
    return [state.copy() for state in self._records]


  def score(self):
    sum = 0
    for state in self._records:
      sum += state.score()
    return sum