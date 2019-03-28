import pytest
from click.testing import CliRunner

from aspr.sim import experiment, spawntimes


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(spawntimes.cli, ['-i', 'cli-test'])
    result = runner.invoke(experiment.cli, ['-s', 'cli-test'])
    assert result.exit_code == 0
    assert 'aspr.experiment.cli' in result.output
    help_result = runner.invoke(experiment.cli, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output
    assert 'Show this message and exit.' in help_result.output
