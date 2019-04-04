# CI Tools

## Development

All the commands are implemented as plugins in the `cctools.commands`
package.  If a python module is placed named "cmd_foo" it will show up as
"foo" command and the `cli` object within it will be loaded as nested
Click command.

### Initialize project

    $ python3 -m venv venv
    $ pip install --editable .
    $ cctools --help
