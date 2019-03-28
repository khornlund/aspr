from aspr.constants import OUTPUTS, SPT_FN
import random, os, click
import numpy as np
from os.path import join, exists

@click.command()
@click.option('-i', '--identifier', required=True, help='Name of new spawntime set')
@click.option('-n', '--n-nodes', type=int, default=20, help = 'Number of nodes to spawn')
@click.option('-t', '--time-window', type=int, default = 50, help = 'Time window over which nodes will spawn.')
@click.option('-s', '--seed', type=int, default = 0, help = 'Random seed to use')
def cli(identifier, n_nodes, time_window, seed):
  stu = SpawnTimeUtil()
  spt = stu.random_unique(n_nodes, time_window, seed)
  spt_folder = join(OUTPUTS, f'{identifier}')
  if exists(spt_folder): raise Exception('Identifier already exists.')
  os.makedirs(spt_folder)
  stu.save(spt, spt_folder)


class SpawnTimeUtil:
  """Tool for generating a set of node spawn times. Can save to file
  and read back out so that models' performance can be compared using
  the same spawn times.
  """
  def save(self, spt, folder):
    with open(join(folder, SPT_FN), 'w') as f:
      f.write('\n'.join([str(s) for s in spt]))


  def read(self, folder):
    path = join(folder, SPT_FN)
    if not exists(path): raise Exception(f'File not found: {path}')
    with open(path, 'r') as f: lines = [int(t) for t in f.readlines()]
    return lines


  def random_unique(self, n, t_win, seed = 0):
    """
    """
    random.seed(seed)
    return list(np.sort(random.sample(range(1, t_win), n)))