import pytest

from aspr.sim.node import Node


@pytest.fixture()
def node():
    return Node(id='test')


@pytest.fixture()
def default_ttl(node):
    return node.ttl


def test_ttl_dec_color_set(node, default_ttl):
    """If a color has been selected, tick should decrease ttl"""
    node.color = 1
    node.tick()
    assert node.ttl == default_ttl - 1


def test_ttl_dec_color_unset(node, default_ttl):
    """If a color has not been selected, tick should NOT decrease ttl"""
    node.tick()
    assert node.ttl == default_ttl


def test_color_reset(node):
    node.color = 1
    node.ttl = 1
    node.tick()
    assert node.color == 1
    node.tick()
    assert node.color == -1
