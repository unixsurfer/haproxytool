#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
# Created by: Pavlos Parissis <pavlos.parissis@booking.com>
#
"""Dump a collection of information about frontends, pools and servers

Usage:
    haproxytool dump [-fpsh -D DIR ]

Options:
    -h, --help                show this screen
    -f, --frontends           show frontends
    -p, --pools               show pool
    -s, --servers             show server
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
    [default: /var/lib/haproxy]

"""
from docopt import docopt
from haproxyadmin import haproxy


def get_pools(hap):
    print("# pool name, status, requests, members")
    for pool in hap.pools():
        members = ','.join([x.name for x in pool.members()])
        print("{},{},{},{}".format(pool.name, pool.status, pool.requests,
                                   members))


def get_frontends(hap):
    print("# frontend name, status, requests, process_nb")
    for frontend in hap.frontends():
        print("{},{},{},{}".format(frontend.name, frontend.status,
                                   frontend.requests, frontend.process_nb))


def get_servers(hap):
    print("# server name, status, requests, pool")
    for server in hap.members():
        print("{},{},{},{}".format(server.name, server.status, server.requests,
                                   server.poolname))


def dump(hap):
    get_frontends(hap)
    get_pools(hap)
    get_servers(hap)


def main():
    arguments = docopt(__doc__)
    hap = haproxy.HAProxy(socket_dir=arguments['--socket-dir'])

    if (not arguments['--frontends'] and not arguments['--pools'] and not
            arguments['--servers']):
        dump(hap)

    if arguments['--frontends']:
        get_frontends(hap)

    if arguments['--pools']:
        get_pools(hap)

    if arguments['--servers']:
        get_servers(hap)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
