import abc, os
import pandas as pd
from aspr.sim.utils import _setup_logger

class LearnerBase(abc.ABC):

  def __init__(self, verbose=0):
    super().__init__()
    self.name = self.__class__.__name__
    self.logger = _setup_logger(self, verbose=verbose)

  @abc.abstractmethod
  def train(self, data_f, **kwargs):
    pass

  @abc.abstractmethod
  def save(self, model, path, **kwargs):
    pass

  @abc.abstractmethod
  def load(self, path, **kwargs):
    pass

  def read_f(self, folder):
    files = [f for f in os.listdir(folder) if '.csv' in f]
    for i, f in enumerate(files):
        tmp_df = pd.read_csv(os.path.join(folder, f), dtype=float)
        if i == 0:
            df = tmp_df
        else:
            df = pd.concat([df, tmp_df], ignore_index=True)
    
    self.logger.info(f'Read {len(df.index)} rows, {len(df.columns)} columns')
    return df
