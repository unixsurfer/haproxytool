#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Created by: Pavlos Parissis <pavlos.parissis@gmail.com>
#
"""A tool to manage HAProxy via the stats socket.

Usage: haproxytool [-v | -h | --socket-dir DIR] <command> [<args>...]

Options:
  -h, --help                show this screen.
  -v, --version             show version.
  -D DIR, --socket-dir=DIR  directory with HAProxy socket files [default: /var/lib/haproxy]

Arguments:
    DIR  a directory path

Available haproxytool commands are:
    frontend  Frontend operations
    backend   Backend operations
    server    Server operations
    dump      Dumps all informations
    map       Manage MAPs

See 'haproxytool help <command>' for more information on a specific command.

"""
from docopt import docopt
from operator import methodcaller


def main():
    args = docopt(__doc__, version='haproxytool 0.2.0', options_first=True)

    call_main = methodcaller('main')

    our_cmds = ['frontend', 'backend', 'server', 'dump', 'haproxy', 'map']
    if args['<command>'] in our_cmds:
        # get module path
        module = __import__('haproxytool.%s' % args['<command>'])
        # get the module object
        module_object = getattr(module, '%s' % args['<command>'])
        # run the main from the module object
        call_main(module_object)
    elif args['<command>'] == 'help':
        if len(args['<args>']) == 1 and args['<args>'][0] in our_cmds:
            module = __import__('haproxytool.%s' % args['<args>'][0])
            module_object = getattr(module, '%s' % args['<args>'][0])
            call_main(module_object)
        else:
            exit("use one of {} in help command".format(','.join(our_cmds)))
    else:
        exit("{} isn't a haproxytool command. See 'haproxytool --help'."
             .format(args['<command>']))

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
