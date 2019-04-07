import click
from click.testing import CliRunner
from cctools.commands.cmd_version import cli


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli, ['raw', '--show', '--file', './tests/stubs/version.txt'])
    assert result.exit_code == 0
    assert '2.5.3' in result.output
