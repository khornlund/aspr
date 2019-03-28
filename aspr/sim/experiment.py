"""Main entry point to perform runs of simulation"""

from aspr.sim.scenario import Scenario
from aspr.sim.decision_model import DecisionModelFactory
from aspr.sim.interference_model import InterferenceModelFactory
from aspr.sim.spawntimes import SpawnTimeUtil
from aspr.sim.utils import _setup_logger
from aspr.constants import OUTPUTS, SPT_FN, DATA
import random, os, click
from os.path import join, exists

@click.command()
@click.option('-s', '--spawn-times', required=True, help='Folder containing spawn times. Generate this using `aspr_spt`.')
@click.option('-c', '--n-colors', default=4, help='Number of node colors available.')
@click.option('-r', '--n-runs', default=1, help='Number of runs to perform.')
@click.option('-dm', '--decision-model', default='greedy', type=click.Choice(DecisionModelFactory.options()))
@click.option('-da', '--decision-model-args', default=None, help='Additional arguments for decision model.')
@click.option('-im', '--interference-model', default='binary', type=click.Choice(InterferenceModelFactory.options()))
@click.option('-ia', '--interference-model-args', default=None, help='Additional arguments for interference model.')
@click.option('-b', '--base-seed', default=0, help='Random seed to use')
@click.option('-v', '--verbose', count=True, help='Log level. Options: -v -vv')
def cli(spawn_times, n_colors, n_runs, decision_model, decision_model_args, 
  interference_model, interference_model_args, base_seed, verbose):
  click.echo("Running aspr.experiment.cli")

  exp = Experiment(
    spt_f = spawn_times,
    nc = n_colors,
    nr = n_runs,
    dm_name = decision_model,
    dm_args = decision_model_args,
    im_name = interference_model,
    im_args = interference_model_args,
    base_seed = base_seed,
    verbose = verbose)
  exp.run()
  return 0


class Experiment:
  """

  Parameters
  ----------
  nn (int) : Number of nodes

  nc (int) : Number of colors

  nr (int) : Number of runs (iterations of scenario)

  spt (list) : Ordered list of integer spawn times

  dm_name (str) : Name of Decision Model to use

  dm_args (dict) : Additional arguments to provide Decision Model

  im_name (str) : Interference Model to use

  im_args (dict) : Additional arguments to provide Interference Model

  out_f (str) : Folder to write output to

  base_seed (int) : Random seed to use

  verbose (int) : Log verbosity. Options: {0: lowest, 1: info, 2: debug}
  """

  def __init__(self, spt_f, nc, nr, dm_name, dm_args, im_name, im_args, 
    base_seed, verbose):

    self.nc = nc
    self.nr = nr
    self.dm_name = dm_name
    self.dm_args = dm_args
    self.im_name = im_name
    self.im_args = im_args
    self.base_seed = base_seed
    self.verbose = verbose

    # construct the path to the spawn times file
    spt_path = join(OUTPUTS, spt_f)
    self.spt = SpawnTimeUtil().read(spt_path)

    self.nn = len(self.spt)

    # subdirectory for number of colors in experiment
    self.exp_f = self._setup_f(spt_path, nc)

    self.name = self.exp_desc()
    self.logger = _setup_logger(self, verbose = verbose)
    self.colors = list(range(self.nc))

    self.dm = DecisionModelFactory().\
      get(self.dm_name, self.colors, self.dm_args, self.verbose)
    self.im = InterferenceModelFactory().\
      get(self.im_name, self.im_args)


  def run(self):
    self.logger.info('..')
    for i in range(self.base_seed + self.nr): self.run_seed(i)


  def run_seed(self, seed):
    self.logger.debug(f'Running seed: {seed}')
    random.seed(seed)
    scenario = Scenario(self.nn, self.spt.copy(), self.colors, self.dm, self.im, 
                        f'{self.name}-{seed}', verbose = self.verbose)
    scenario.run()
    scenario.to_df().to_csv(
      join(self.exp_f, f'{scenario.name}.csv'), index = False)


  def _setup_f(self, base, nc):
    exp_f = join(base, f'nc{nc}', DATA, self.exp_desc())
    if not os.path.exists(exp_f):
      os.makedirs(exp_f)
    return exp_f


  def exp_desc(self):
    return '-'.join([f'{self.dm_name}', f'{self.im_name}'])

    
