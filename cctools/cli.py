import os
import sys
import click

from cctools.context import pass_context
from cctools.commands.changelog.commands import changelog
from cctools.commands.version.commands import cli as version

CONTEXT_SETTINGS = dict(auto_envvar_prefix='CCTOOLS')


class Context(object):

    def __init__(self):
        self.verbose = False

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)



@click.group()
@pass_context
def cli(ctx):
    pass


cli.add_command(changelog)
cli.add_command(version)
