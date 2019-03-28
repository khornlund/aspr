""" CLI for training models"""

import os, click
from aspr.model.linreg import LinearRegressorLearner
from aspr.model.features import FeatureExtractor
from aspr.constants import SPT_FN
from os.path import join, exists

@click.command()
@click.option('-m', '--model-name', required=True, help='Model to train')
@click.option('-f', '--folder', required=True, help='Folder to use for training')
@click.option('-c', '--n-colors', type=int, required=True, help='Number of colors in scenario')
@click.option('-v', '--verbose', count=True, help='Log level. Options: -v -vv')
def cli(model_name, folder, n_colors, verbose):
  colors = range(n_colors)
  feat_f = make_features(folder, colors, verbose)
  model = get_model(model_name, colors, verbose)
  model.train(feat_f)


def get_model(model_name, colors, verbose):
  if model_name == 'linreg':
    return LinearRegressorLearner(colors, verbose)


def make_features(folder, colors, verbose):
  spt_f = join(folder, '..', '..', '..')
  fe = FeatureExtractor(join(spt_f, SPT_FN), verbose)
  dest_folder = f'{folder}-feat'
  if exists(dest_folder):
    return dest_folder
    
  os.makedirs(dest_folder)
  for csv_file in [f for f in os.listdir(folder) if '.csv' in f]: 
    feat_df = fe.extract(os.path.join(folder, csv_file))
    save_as = os.path.join(dest_folder, csv_file)
    feat_df.to_csv(save_as, index=False)
  return dest_folder