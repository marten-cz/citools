# CI Tools

[![pypi](https://img.shields.io/pypi/v/cctools.svg)](https://pypi.org/project/cctools/)
[![travis](https://travis-ci.org/marten-cz/citools.svg?branch=master)](https://travis-ci.org/marten-cz/citools/)
[![codecov](https://codecov.io/gh/marten-cz/citools/branch/master/graph/badge.svg)](https://codecov.io/gh/marten-cz/citools)

## Development

All the commands are implemented as plugins in the `cctools.commands`
package.  If a python module is placed named "cmd_foo" it will show up as
"foo" command and the `cli` object within it will be loaded as nested
Click command.

### Initialize project

    $ python3 -m venv venv
    $ pip install --editable .
    $ cctools --help

### Tests

To run tests locally start

    $ tox
