#! /usr/bin/env python
# vim:fenc=utf-8
"""A tool to manage HAProxy via the stats socket.

Usage: haproxytool [-v | -h] <command> [<args>...]

Options:
  -h, --help                show this screen.
  -v, --version             show version.

Available haproxytool commands:
    haproxy   HAProxy operations
    frontend  Frontend operations
    backend   Backend operations
    server    Server operations
    dump      Dumps all informations
    map       Manage MAPs
    acl       Manage ACLs

See 'haproxytool help <command>' for more information on a specific command.

"""
import sys
from operator import methodcaller
from importlib import import_module
from docopt import docopt
from haproxytool import __version__ as version
from haproxytool import OUR_CMDS


def main():
    """
    Parse top level CLI interface and invoke subcommand
    """
    args = docopt(__doc__, version=version, options_first=True)

    call_main = methodcaller('main')

    if args['<command>'] in OUR_CMDS:
        sub_cmd = import_module('haproxytool.%s' % args['<command>'])
        call_main(sub_cmd)
    elif args['<command>'] == 'help':
        if len(args['<args>']) == 1 and args['<args>'][0] in OUR_CMDS:
            sub_cmd = import_module('haproxytool.%s' % args['<args>'][0])
            call_main(sub_cmd)
        else:
            msg = "use any of {c} in help command".format(c=','.join(OUR_CMDS))
            sys.exit(msg)
    else:
        sys.exit("<{}> isn't a haproxytool command. See 'haproxytool --help'."
                 .format(args['<command>']))

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
