#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
# Created by: Pavlos Parissis <pavlos.parissis@gmail.com>
#
"""Dump a collection of information about frontends, backends and servers

Usage:
    haproxytool dump [-fbsh -D DIR ]

Options:
    -h, --help                show this screen
    -f, --frontends           show frontends
    -b, --backends            show backends
    -s, --servers             show servers
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
    [default: /var/lib/haproxy]

"""
import sys
from docopt import docopt
from haproxyadmin import haproxy
from haproxyadmin.exceptions import (SocketApplicationError,
                                     SocketConnectionError,
                                     SocketPermissionError)


def get_backends(hap):
    print("# backend name, status, requests, servers")
    for backend in hap.backends():
        servers = ','.join([x.name for x in backend.servers()])
        print("{},{},{},{}".format(backend.name, backend.status,
                                   backend.requests, servers))


def get_frontends(hap):
    print("# frontend name, status, requests, process_nb")
    for frontend in hap.frontends():
        print("{},{},{},{}".format(frontend.name, frontend.status,
                                   frontend.requests, frontend.process_nb))


def get_servers(hap):
    print("# server name, status, requests, backend")
    for server in hap.servers():
        print("{},{},{},{}".format(server.name, server.status, server.requests,
                                   server.backendname))


def dump(hap):
    get_frontends(hap)
    get_backends(hap)
    get_servers(hap)


def main():
    arguments = docopt(__doc__)
    args_passed = False

    try:
        hap = haproxy.HAProxy(socket_dir=arguments['--socket-dir'])
    except (SocketApplicationError,
            SocketConnectionError,
            SocketPermissionError) as error:
        print(error, error.socket_file)
        sys.exit(1)
    except ValueError as error:
        print(error)
        sys.exit(1)

    if arguments['--frontends']:
        args_passed = True
        get_frontends(hap)

    if arguments['--backends']:
        args_passed = True
        get_backends(hap)

    if arguments['--servers']:
        args_passed = True
        get_servers(hap)

    if not args_passed:
        dump(hap)
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
