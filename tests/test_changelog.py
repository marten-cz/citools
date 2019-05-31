import os
import yaml
from distutils.dir_util import copy_tree
from click.testing import CliRunner
from cctools.commands.changelog.commands import changelog


def test_create_changelog(tmpdir):
    tmpdir = str(tmpdir)
    runner = CliRunner()
    result = runner.invoke(changelog, ['add', '--task', '234', '-m', 'Test message', '--type', 'added', '--dir', tmpdir, '--file', 'aaa.yml'])
    file = os.path.realpath(os.path.join(str(tmpdir), 'unreleased', 'aaa.yml'))
    assert result.output == ''
    assert result.exit_code == 0
    assert os.path.isfile(file)
    with open(file, 'r') as stream:
        data = yaml.load(stream, Loader=yaml.FullLoader)
        expected = [{'task': '234', 'title': 'Test message', 'type': 'added'}]
        assert all([sorted(a) == sorted(b) for a, b in zip(sorted(data), sorted(expected))])

def test_release_changelog(tmpdir):
    tmpdir = str(tmpdir)
    copy_tree('./tests/stubs/changelogs/1/', os.path.join(tmpdir, 'unreleased'))
    assert os.path.isfile(os.path.join(tmpdir, 'unreleased', 'test.yml'))
    runner = CliRunner()
    result = runner.invoke(changelog, ['release', '9.0.2', '--dir', tmpdir])
    file = os.path.realpath(os.path.join(str(tmpdir), 'released', '9.0.2.yml'))
    assert result.output == ''
    assert result.exit_code == 0
    assert os.path.isfile(file)
    assert not os.path.isfile(os.path.join(tmpdir, 'unreleased', 'test.yml'))
    with open(file, 'r') as stream:
        data = yaml.load(stream, Loader=yaml.FullLoader)
        expected = [{'task': '234', 'title': 'Test message', 'type': 'added'}]
        assert all([sorted(a) == sorted(b) for a, b in zip(sorted(data), sorted(expected))])
