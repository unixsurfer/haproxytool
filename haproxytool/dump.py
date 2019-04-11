#!/usr/bin/env python
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
"""Dump a collection of information about frontends, backends and servers

Usage:
    haproxytool dump [-D DIR | -F SOCKET] [-fbsh]

Arguments:
    SOCKET  Socket file

Options:
    -f, --frontends           show frontends
    -F SOCKET, --file SOCKET  socket file
    -b, --backends            show backends
    -s, --servers             show servers
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                              [default: /var/lib/haproxy]

"""
from docopt import docopt

from .utils import haproxy_object


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
    hap = haproxy_object(arguments)

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
