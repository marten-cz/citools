import os
import uuid
import yaml

import click
from datetime import date
from jinja2 import Template

from cctools.context import pass_context


@click.group()
def changelog():
    pass


@changelog.command('add', short_help='Add new line to the changelog')
@click.option('--dir', default='./changelogs/', required=False, type=click.Path(exists=False, file_okay=False),
              help='File to use to store the version data.')
@click.option('-m', '--message', required=False, type=str,
              help='Message to use')
@click.option('--task', '--issue', required=False, type=str,
              help='Issue number')
@click.option('-t', '--type', required=False, default='added', type=click.Choice(
    ['added', 'fixed', 'changed', 'deprecated', 'removed', 'security', 'performance', 'other']),
              help='The category of the change')
@click.option('-f', '--file', required=False, default=None,
              help='Filename')
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@pass_context
def add(ctx,
        dir, # type: str
        message, # type: str
        task, # type: str
        type, # type: str
        file, # type: str
        verbose # type: bool
        ):
    """
    Create and work with changelog files

    :param ctx:
    :param dir:
    :param message:
    :param task:
    :param type:
    :param verbose:
    :return:
    """

    #create_markdown('./tests/stubs/expected/release.yml')
    #return
    ctx.verbose = verbose
    unreleased_path = os.path.realpath(os.path.join(os.getcwd(), dir, 'unreleased'))

    os.makedirs(unreleased_path, exist_ok=True)
    branch = vcs_get_branch()
    new_file = os.path.realpath(os.path.join(unreleased_path, file if file else (branch if branch else uuid.uuid4().hex) + '.yml'))
    ctx.vlog('create {}'.format(new_file))

    try:
        data = load_yaml(new_file)
        with open(new_file, 'w+') as stream:
            if not data:
                data = {'details': []}
            if 'details' not in data:
                data['details'] = []

            data['details'] = update_change_list(data['details'], type, {'title': estr(message), 'task': estr(task)})
            stream.write(yaml.dump(data, Dumper=yaml.Dumper))
    except yaml.YAMLError as exc:
        raise click.ClickException('Error when reading yaml file')


@changelog.command('release', short_help='Release all changelogs as new version')
@click.argument('version', required=True, type=str)
@click.option('--dir', default='./changelogs/', required=False, type=click.Path(exists=False, file_okay=False),
              help='File to use to store the version data.')
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@pass_context
def release(ctx,
            version, # type: str
            dir, # type: str
            verbose # type: bool
            ):
    """
    Create and work with changelog files

    :param ctx:
    :param version:
    :param dir:
    :param verbose:
    :return:
    """
    ctx.verbose = verbose
    unreleased_path = os.path.realpath(os.path.join(os.getcwd(), dir, 'unreleased'))

    version_path = os.path.realpath(os.path.join(os.getcwd(), dir, 'released'))
    os.makedirs(version_path, exist_ok=True)
    data = []
    for file in os.listdir(unreleased_path):
        data.extend(load_yaml(os.path.realpath(os.path.join(unreleased_path, file))))
    with open(os.path.join(version_path, version + '.yml'), 'w') as stream:
        full_data = {
            'version': version,
            'date': date.today().strftime("%Y-%m-%d %H:%M:%S"),
            'details': data
        }
        stream.write(yaml.dump(full_data, Dumper=yaml.Dumper))

    for file in os.listdir(unreleased_path):
        os.remove(os.path.join(unreleased_path, file))


def update_change_list(details, type, change):
    for detail in details:
        if detail['type'] == type:
            detail['changes'].append(change)
            return details

    details.append({'type': type, 'changes': [change]})

    return details


def create_markdown(file):
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates/one-version.jj2'), 'r') as stream:
        template = Template(stream.read())
        data = load_yaml(file)
        result = template.render(release=data)


def load_yaml(file) -> dict:
    try:
        with open(file, 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)
            #data = list()
            #if not data:
            #elif not isinstance(data, list):
            #    raise click.ClickException('Unsupported content in {}'.format(file))
        return data
    except FileNotFoundError:
        return {}


def estr(s):
    return '' if s is None else str(s)


def vcs_get_branch(vcs: str = 'git'):
    if vcs is 'git':
        return os.popen('git branch | grep \\* | cut -d \' \' -f2').read().strip()

