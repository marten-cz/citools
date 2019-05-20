import os
import uuid
import yaml

import click
from cctools.cli import pass_context


@click.command('changelog', short_help='Operations around changelog.')
@click.argument('action', required=False, type=click.Choice(['add', 'release']))
@click.option('--dir', default='./changelogs/', required=False, type=click.Path(exists=False, file_okay=False),
              help='File to use to store the version data.')
@click.option('-m', '--message', required=False, type=str,
              help='Message to use')
@click.option('--task', '--issue', required=False, type=str,
              help='Issue number')
@click.option('--version', required=False, type=str,
              help='Version number')
@click.option('-t', '--type', required=False, default='added', type=click.Choice(
    ['added', 'fixed', 'changed', 'deprecated', 'removed', 'security', 'performance', 'other']),
              help='The category of the change')
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@pass_context
def cli(ctx, action: str, dir: str, message: str, task: str, type: str, verbose, version: str):
    """
    Create and work with changelog files

    :param ctx:
    :param action:
    :param dir:
    :param message:
    :param task:
    :param type:
    :param verbose:
    :param version:
    :return:
    """
    ctx.verbose = verbose
    unreleased_path = os.path.realpath(os.path.join(os.getcwd(), dir, 'unreleased'))

    if action == 'add':
        os.makedirs(unreleased_path, exist_ok=True)
        branch = vcs_get_branch()
        new_file = os.path.realpath(os.path.join(unreleased_path, (branch if branch else uuid.uuid4().hex) + '.yml'))
        ctx.vlog('create {}'.format(new_file))

        try:
            data = load_yaml(new_file)
            with open(new_file, 'w') as stream:
                data.append({'title': estr(message), 'task': estr(task), 'type': estr(type)})
                stream.write(yaml.dump(data, Dumper=yaml.Dumper))
        except yaml.YAMLError as exc:
            raise click.ClickException('Error when reading yaml file')

    elif action == 'release':
        version_path = os.path.realpath(os.path.join(os.getcwd(), dir, 'released'))
        os.makedirs(version_path, exist_ok=True)
        data = []
        for file in os.listdir(unreleased_path):
            data.extend(load_yaml(os.path.realpath(os.path.join(unreleased_path, file))))
        with open(os.path.join(version_path, version + '.yml'), 'w') as stream:
            stream.write(yaml.dump(data, Dumper=yaml.Dumper))


def load_yaml(file) -> list:
    with open(file, 'r') as stream:
        data = yaml.load(stream, Loader=yaml.FullLoader)
        if not data:
            data = list()
        elif not isinstance(data, list):
            raise click.ClickException('Unsupported content in {}'.format(file))
    return data


def estr(s):
    return '' if s is None else str(s)


def vcs_get_branch(vcs: str = 'git'):
    if vcs is 'git':
        return os.popen('git branch | grep \\* | cut -d \' \' -f2').read().strip()
