import numpy as np
import pandas as pd
from aspr.model.linreg import LinearRegressorLearner
from aspr.sim.state import State, StateStatistics, History
from aspr.sim.utils import _setup_logger
import copy, os, abc, weakref

class DecisionModelBase(abc.ABC):
  """"""
  def __init__(self, colors, verbose=0):
    #super().__init__() #TODO: this breaks double inheritance
    self.name = self.__class__.__name__
    self.colors = colors
    self.logger = _setup_logger(self, verbose = verbose)


  @abc.abstractmethod
  def decide(self, history):
    pass


class DecisionModelFactory:
  """"""
  @staticmethod
  def options(): return ['greedy', 'random', 'rrobin', 'linreg']


  def get(self, name, colors, aarg, verbose):
    if name == 'greedy':
      return GreedyDecision(colors, aarg, verbose)
    if name == 'random':
      return RandomDecision(colors, verbose)
    if name == 'rrobin':
      return RoundRobinDecision(colors, verbose)
    if name == 'linreg':
      return LinearRegressor(colors, aarg, verbose)


class LinearRegressor(DecisionModelBase, LinearRegressorLearner):
  """
  """
  def __init__(self, colors, exp_f, verbose=0):
    super().__init__(colors, verbose)
    super().__init__(colors, verbose)
    
    self.colors = colors
    self.regrs = self.load(exp_f)
    self.logger.debug(f'<init>: colors={colors}, model={self.regrs}')


  def decide(self, history):
    # get features from state
    feat = self.get_feat_df(history)
    df = pd.DataFrame({k: [v] for k,v in feat.items()})

    df = df[[col for col in df.columns if col in self.features]]

    self.logger.debug(f'Predicting: {df.head()}')

    preds = []
    for c in self.colors:
      df['decision'] = c
      pred_loss = self.regrs[c].predict(df)
      preds.append(pred_loss)

    decision = preds.index(min(preds))
    self.logger.debug(f'Predicted loss = {preds}, decision = {decision}')
    return decision


  def get_feat_df(self, history):
    state = history.read(-1)
    feat = state.to_dict()
    return feat


class GreedyDecision(DecisionModelBase):
  """Will choose the color that results in the lowest cumulative
  score over the next ps ticks.
  """
  def __init__(self, colors, ps, verbose=0):
    super().__init__(colors, verbose)
    self.ps = int(ps) if ps != None else 1
    self.logger.debug('<init>: colors={}, ps={}, verbose={}'.format(
      self.colors, self.ps, verbose
    ))


  def peek_cum_score(self, state, color, ps):
    temp_state = state.copy()
    temp_state.activate(color)
    temp_score = temp_state.score()
    for _ in range(ps - 1):
      temp_state.tick()
      temp_score += temp_state.score()
    return temp_score


  def min_score_color(self, scores):
    min_score = np.inf
    min_color = -1

    for color, score in scores:
      if score < min_score:
        min_score = score
        min_color = color
    
    return min_color


  def decide(self, history):
    state = history.read()[-1]
    state.tick() # look one step ahead
    scores = [(c, self.peek_cum_score(state, c, self.ps))
      for c in self.colors]
    decision = self.min_score_color(scores)
    self.logger.debug(f'Scores: {scores}')
    self.logger.debug(f'Selected: c={decision}')
    return decision


class RandomDecision(DecisionModelBase):
  """Will return a random color."""

  def __init__(self, colors, verbose=0):
    super().__init__(colors, verbose)


  def decide(self, history):
    decision = self.colors[np.random.randint(0, len(self.colors))]
    self.logger.debug(f'Selected: c={decision}')
    return decision


class RoundRobinDecision(DecisionModelBase):
  """Will iterate through possible colors with each call to decide()"""
  
  def __init__(self, colors, verbose=0):
    super().__init__(colors, verbose)
    self.next = -1


  def decide(self, history):
    self.next = (self.next + 1) % len(self.colors)
    decision = self.colors[self.next]
    self.logger.debug(f'Selected: c={decision}')
    return decision