import pytest
from aspr.sim.decision_model import GreedyDecision

def test_min_score_color_01():
  gdm = GreedyDecision(colors = [0, 1, 2, 3], ps=1)
  scores = [
    (0, 15),
    (1, 9),
    (2, 5),
    (3, 11)]
  assert gdm.min_score_color(scores) == 2

def test_min_score_color_02():
  gdm = GreedyDecision(colors = [0, 1, 2, 3], ps=1)
  scores = [
    (0, 15),
    (1, 9),
    (2, 16),
    (3, 11)]
  assert gdm.min_score_color(scores) == 1
