from aspr.sim.utils import _setup_logger
from aspr.sim.state import State, StateStatistics, History
from aspr.model.learner import LearnerBase
from aspr.constants import DATA, MODELS, MDL_EXT, OUTPUTS
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import os, joblib, click
from os.path import join, exists


class LinearRegressorLearner(LearnerBase):
  """
  """

  @property
  def features(self):
    features = []
    features.extend([f'c{c}-n-active' for c in self.colors])
    features.extend([f'c{c}-total-ttl' for c in self.colors])
    features.extend(['decision', 'loss'])
    return features


  def __init__(self, colors, verbose=0):
    super().__init__(verbose=verbose)
    self.colors = colors
    self.logger.debug('<init>')


  def train(self, data_f, **kwargs):
    self.logger.info(f'Training from: {data_f}')
    df = self.read_f(data_f)
    df = df[[col for col in df.columns if col in self.features]]

    missing = [f for f in self.features if f not in df.columns]
    if missing:
      self.logger.warning(f'Missing features: {missing}')

    regrs = {}

    for c in self.colors:
      self.logger.info(f'Training for color: {c}')
      c_df = df.loc[df['decision'] == c,:]
      y_col = 'loss'
      X_cols = [col for col in c_df.columns if col != y_col]

      X_train, X_test, y_train, y_test = train_test_split(
        c_df[X_cols], c_df[y_col], test_size = 0.2, random_state = 42)

      regr = LinearRegression()
      regr.fit(X_train, y_train)
      y_pred = regr.predict(X_test)

      self.logger.debug(f'Coefficients: \n{regr.coef_}')
      self.logger.debug(f'Mean squared error: {mean_squared_error(y_test, y_pred)}')
      self.logger.debug(f'Variance score: {r2_score(y_test, y_pred)}')

      out_f = self.model_out_f(data_f)
      if not exists(out_f): os.makedirs(out_f)
      self.save(regr, os.path.join(out_f, f'{c}{MDL_EXT}'))
      regrs[c] = regr

    self.logger.info('Done!') 
    return regrs


  def model_out_f(self, data_f):
    out_f = join(data_f, '..', '..', MODELS, 'linreg')
    return out_f


  def save(self, model, path, **kwargs):
    self.logger.info(f'Saving: {path}')
    joblib.dump(model, path)


  def load(self, exp_f, **kwargs):
    path = join(OUTPUTS, exp_f, f'nc{len(self.colors)}', MODELS, 'linreg')
    regrs = {}
    for c in self.colors:
      f = join(path, f'{c}{MDL_EXT}')
      self.logger.info(f'Loading: {f}')
      regrs[c] = joblib.load(f)
    return regrs




 




