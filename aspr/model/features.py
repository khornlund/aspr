import pandas as pd
import numpy as np
import os, glob, click
from aspr.sim.utils import _setup_logger
from aspr.constants import NODE_TTL

@click.command()
@click.option('-f', '--folder', required=True, help='Folder to generate feature .csv for')
@click.option('-c', '--n-colors', type=int, required=True, help='Number of colors in scenario')
@click.option('-n', '--n-nodes', type=int, required=True, help='Number of nodes in scenario')
@click.option('-s', '--spawn-times-file', required=True, help='Spawn times file')
@click.option('-v', '--verbose', count=True, help='Log level. Options: -v -vv')
def cli(folder, n_colors, n_nodes, spawn_times_file, verbose):
  """Extracts features for supervised learning from scenario records"""
  dest_folder = f'{folder}-feat'
  if not os.path.exists(dest_folder): os.makedirs(dest_folder)

  csv_files = [f for f in os.listdir(folder) if '.csv' in f]

  fe = FeatureExtractor(spawn_times_file, verbose)

  for csv_file in csv_files: 
    feat_df = fe.extract(os.path.join(folder, csv_file))
    save_as = os.path.join(dest_folder, csv_file.replace('.csv', '-feat.csv'))
    feat_df.to_csv(save_as, index=False)


class FeatureExtractor:
  """
  """
  def __init__(self, spt_f, verbose = 0):
    with open(spt_f, 'r') as f: 
      self.spt = [int(t) for t in f.readlines()]
    self.name = 'FeatureExtractor'
    self.logger = _setup_logger(self, verbose = verbose)
    self.logger.debug('<init>')

  def extract(self, csv_f):
    """Extract the decision points from the .csv log of a simulation"""
    self.logger.info(f'extracting: {csv_f}')
    df = pd.read_csv(csv_f, dtype=int)
    df['decision'] = -1
    df['loss'] = 0
    for spawn_num, t_index in enumerate(self.spt):
      df.loc[t_index-1, 'decision'] = df.loc[t_index, f'n{spawn_num}-color']
      df.loc[t_index-1, 'loss'] = self.loss_for_decision(df, spawn_num, t_index)
        
    n_active_cols = [col for col in df.columns if 'n-active' in col]
    total_ttl_cols = [col for col in df.columns if 'total-ttl' in col]
    feat_df = df.loc[self.spt, n_active_cols + total_ttl_cols + ['score', 'decision', 'loss']]
    return feat_df
      
  
  def loss_for_decision(self, df, spawn_num, t_index):
    """compute the interference score (loss) due to decision
    
    This is computed as: the mean interference delta over the ttl
    of the activated node.
    
    Eg. if the current interference is 5, and the interference scores
    for the next 10 steps are: [6, 6, 7, 5, 8, 8, 8, 7, 7, 6]
    then the score is mean([6, 6, 7, 5, 8, 8, 8, 7, 7, 6])-5
    """
    ttl = NODE_TTL
    init_score = df.loc[t_index-1, 'score']
    ttl_scores = df.loc[t_index:t_index+ttl, 'score']
    return np.mean(ttl_scores)-init_score

        

  