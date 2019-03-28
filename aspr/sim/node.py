from aspr.constants import NODE_TTL

class Node:
  """
  """
  def __init__(self, id):
    self.id = id
    self.color = -1
    self.ttl = NODE_TTL


  def tick(self):
    if self.ttl <= 0 and self.color != -1:
      self.color = -1
    elif self.color >= 0:
      self.ttl -= 1


  def to_dict(self):
    attrs = ['color', 'ttl']
    return {f'n{self.id}-{attr}': getattr(self, attr) for attr in attrs}