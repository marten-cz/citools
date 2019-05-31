import os
import click
from cctools.context import pass_context

action_number = {
    'major': 0,
    'minor': 1,
    'patch': 2
}


@click.command('version', short_help='Read and update version file.')
@click.argument('language', required=True, type=click.Choice(['raw', 'npm']))
@click.option('--file', required=False, type=click.Path(exists=True, file_okay=True),
              help='File to use to store the version data.')
@click.option('--show', 'action', default=True, flag_value='show',
              help='Show current version.')
@click.option('--major', 'action', flag_value='major',
              help='Increment major version.')
@click.option('--minor', 'action', flag_value='minor',
              help='Increment minor version.')
@click.option('--patch', 'action', flag_value='patch',
              help='Increment patch version.')
@click.option('--vcs-add/--no-vcs-add', 'vcs', default=False,
              help='Set to add the change to VCS as commit.')
@click.option('--vcs-add/--no-vcs-add', 'vcs', default=False,
              help='Set to add the change to VCS as commit.')
@pass_context
def cli(ctx, language: str, file: str, action: str, vcs: bool):
    """
    Get or increment current version in the file

    Supported: raw text file, npm package.json

    :param ctx:
    :param language:
    :param file:
    :param action:
    :param vcs:
    :return:
    """
    new_version = None
    vcs_files = []

    if language == 'raw':
        with open(file) as f:
            version = f.read()
        if action == 'show':
            ctx.log('{}'.format(version))
            return
        new_version = increment_version(version, action_number[action])
        with open(file, 'w') as f:
            f.write(new_version)
            vcs_files.append(file)
    elif language == 'npm':
        version = os.popen('node -p "require(\'{}\').version"'.format(file if file else './package.json')).read()
        if action == 'show':
            ctx.log('{}'.format(version))
            return
        new_version = increment_version(version, action_number[action])
        os.popen('yarn version --{} --no-git-tag-version'.format(action)).read()

    if vcs is True:
        vcs_add('svn', vcs_files)

    if new_version is not None:
        ctx.log('{}'.format(new_version))
    else:
        ctx.log('Error when updating the version number')


def increment_version(version: str, position: int = 2):
    version = version.strip().split('.')
    version[position] = str(int(version[position]) + 1)
    return '.'.join(version)


def vcs_add(vcs: str, files: list = None):
    if list is None:
        return

    if vcs is 'git':
        os.popen('git add {}'.format(' '.join(files))).read()
    else:
        raise click.ClickException('Unknown version control{}'.format(' {}'.format(vcs) if vcs else ''))
