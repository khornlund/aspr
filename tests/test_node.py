import pytest
from aspr.sim.node import Node

def test_ttl_dec_01():
  n = Node(id = 'test')
  default_ttl = n.ttl
  n.color = 1
  n.tick()
  assert n.ttl == default_ttl - 1

def test_ttl_dec_02():
  n = Node(id = 'test')
  default_ttl = n.ttl
  n.tick()
  assert n.ttl == default_ttl

def test_color_reset_01():
  n = Node(id = 'test')
  n.color = 1
  n.ttl = 1
  n.tick()
  assert n.color == 1
  n.tick()
  assert n.color == -1
