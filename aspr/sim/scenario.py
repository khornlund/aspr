import pandas as pd
import numpy as np
import copy
from aspr.sim.state import State, History
from aspr.sim.utils import _setup_logger

class Scenario:
  """This class encapsulates a single simulation from beginning to end.

  The scenario will iterate through units of time. At given spawn times,
  nodes will be activated and assigned a color, as given by the decision model.

  Nodes activated will incur an interference cost per unit time based 
  on their color, as given by the interference model.

  The state of the scenario is saved at each unit of time, and can be
  accessed upon completion using .to_csv()

  Parameters
  ----------

  n_nodes : int
    Number of nodes which may be activated during the scenario

  spt : int
    The times at which nodes will be activated.

  dec_model : DecisionModel
    The decision model to use when choosing which color to assign an activating node.

  int_model : InterferenceModel
    The model to use for evaluating the interference score between two active nodes.

  verbose : int
    The log level. {0: None, 1: Info, 2: Debug}

  name : str
    The name for the logger to use.
  """
  def __init__(self, n_nodes, spt, colors, dec_model, int_model, name,
    verbose=0):
    self.state = State().init(n_nodes, int_model, colors, verbose = verbose)
    self.history = History(self.state)
    self.spt = spt
    self.colors = colors
    self.dec_model = dec_model
    self.name = name
    self.logger = _setup_logger(self, verbose=verbose)
    self.logger.debug('<init>')


  def run(self):
    self.logger.info('Starting...')
    self.logger.debug(f'Spawn times: {self.spt}')
    next_spawn = self.spt.pop(0)

    while True:
      # all nodes update their state
      self.logger.debug(f'Tick: t={self.state.t}')
      self.state.tick()

      # check for new node activations
      if self.state.t == next_spawn:
        self.logger.debug(f'Spawn at t={self.state.t}')
        decision = self.dec_model.decide(self.history)
        self.state.activate(decision)
        if self.spt:
          self.logger.debug(f'Remaining spt: {self.spt}')
          next_spawn = self.spt.pop(0)

      # record state
      self.history.record(self.state)

      # exit if all time-to-live expired
      if self.state.all_nodes_expired():
        return self.end_run('All nodes TTL expired.')

      # exit if no more spawns, and all activated nodes ttl expired
      if self.all_spawns_complete(self.spt, self.state):
        return self.end_run('All spawns complete.')


  def all_spawns_complete(self, spt, state):
    spawn_fin = not spt
    active_nodes = state.count_active_nodes()
    return spawn_fin and active_nodes == 0


  def end_run(self, m):
    # perform one last tick and record
    self.state.tick()
    self.history.record(self.state)
    self.logger.info('Simulation complete: %s' % m)


  def score(self):
    return self.history.score()


  def to_df(self):
    d = [state.to_dict() for state in self.history.read()]
    df = pd.DataFrame(d)
    df.set_index('t', inplace=True)
    return df




