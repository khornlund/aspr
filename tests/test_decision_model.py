import pytest

from aspr.sim.decision_model import GreedyDecision

@pytest.fixture()
def greedy_dec_model():
    return GreedyDecision(colors = [0, 1, 2, 3], ps=1)


@pytest.mark.parametrize('scores, exp_min', [
    (
        [
            (0, 15),
            (1, 9),
            (2, 5),
            (3, 11)
        ],
        2
    ),
    (
        [
            (0, 15),
            (1, 9),
            (2, 16),
            (3, 11)
        ],
        1
    ),
])
def test_min_score_color_01(greedy_dec_model, scores, exp_min):
  assert greedy_dec_model.min_score_color(scores) == exp_min

