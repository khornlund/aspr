import abc
import numpy as np

class InterferenceModel(abc.ABC):
  
  def __init__(self):
    super().__init__()

  @abc.abstractmethod
  def calc(self, u, v):
    pass


class InterferenceModelFactory:

  @staticmethod
  def options(): return ['binary']

  def get(self, name, *args):
    if name == 'binary':
      return BinaryInterference()



class BinaryInterference(InterferenceModel):

  def calc(self, u, v):
    if u.id != v.id and u.color >= 0 and u.color == v.color:
      return 1
    else:
      return 0

