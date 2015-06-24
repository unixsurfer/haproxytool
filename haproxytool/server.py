#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
# Created by: Pavlos Parissis <pavlos.parissis@gmail.com>
#
"""Manage servers

Usage:
    haproxytool server [-D DIR | -h] (-r | -s | -e | -d | -R | -n | -t | -p | -W | -i) [--backend=<name>...] [NAME...]
    haproxytool server [-D DIR | -h] -w VALUE [--backend=<name>...] [NAME...]
    haproxytool server [-D DIR | -h] (-l | -M)
    haproxytool server [-D DIR | -h] -m METRIC [--backend=<name>...] [NAME...]


Arguments:
    DIR     Directory path
    VALUE   Value to set
    METRIC  Name of a metric, use '-M' to get metric names

Options:
    -h, --help                show this screen
    -e, --enable              enable server
    -d, --disable             disable server
    -R, --ready               set server in normal mode
    -n, --drain               drain server
    -t, --maintenance         set server in maintenance mode
    -r, --requests            show requests
    -p, --process             show process number
    -i, --sid                 show server ID
    -s, --status              show status
    -m, --metric              show value of a metric
    -M, --list-metrics        show all metrics
    -l, --list                show all servers
    -w, --weight              change weight for server
    -W, --get-weight          show weight of server
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
    [default: /var/lib/haproxy]

"""
import sys
from docopt import docopt
from haproxyadmin import haproxy, exceptions
from operator import methodcaller
from haproxyadmin.exceptions import (SocketApplicationError,
                                     SocketConnectionError,
                                     SocketPermissionError)


def build_server_list(hap, names=None, backends=None):
    servers = []
    if not names:
        if not backends:
            for server in hap.servers():
                servers.append(server)
        else:
            for backend in backends:
                for server in hap.servers(backend):
                    servers.append(server)
    else:
        if not backends:
            for name in names:
                try:
                    for server in hap.server(name):
                        servers.append(server)
                except ValueError:
                    print("{} was not found".format(name))
        else:
            for backend in backends:
                for name in names:
                    try:
                        for server in hap.server(name, backend):
                            servers.append(server)
                    except ValueError:
                        print("{} was not found".format(name))

    if not servers:
        sys.exit(1)

    return servers


def list_servers(servers):
    print("# backendname servername")
    for server in servers:
        print("{:<30} {}".format(server.backendname, server.name))


def status(servers):
    print("# backendname servername")
    for server in servers:
        print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                        server.status))


def requests(servers):
    print("# backendname servername")
    for server in servers:
        print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                        server.requests))


def sid(servers):
    print("# backendname servername")
    for server in servers:
        print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                        server.sid))


def process(servers):
    print("# backendname servername")
    for server in servers:
        print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                        server.process_nb))


def enable(servers):
    for server in servers:
        try:
            server.setstate(haproxy.STATE_ENABLE)
            print("{} enabled in {} backend".format(server.name,
                                                    server.backendname))
        except exceptions.CommandFailed as error:
            print("{} failed to be enabled:{}".format(server.name, error))


def disable(servers):
    for server in servers:
        try:
            server.setstate(haproxy.STATE_DISABLE)
            print("{} disabled in {} backend".format(server.name,
                                                     server.backendname))
        except exceptions.CommandFailed as error:
            print("{} failed to be disabled:{}".format(server.name, error))


def ready(servers):
    for server in servers:
        try:
            server.setstate(haproxy.STATE_READY)
            print("{} set to ready in {} backend".format(server.name,
                                                         server.backendname))
        except exceptions.CommandFailed as error:
            print("{} failed to set normal state:{}".format(server.name,
                                                            error))


def drain(servers):
    for server in servers:
        try:
            server.setstate(haproxy.STATE_DRAIN)
            print("{} set to drain in {} backend".format(server.name,
                                                         server.backendname))
        except exceptions.CommandFailed as error:
            print("{} failed to set in drain state:{}".format(server.name,
                                                              error))


def maintenance(servers):
    for server in servers:
        try:
            server.setstate(haproxy.STATE_READY)
            print("{} set to ready in {} backend".format(server.name,
                                                         server.backendname))
        except exceptions.CommandFailed as error:
            print("{} failed to set to maintenance state:{}".format(server.name,
                                                                    error))


def weight(servers, value):
    try:
        value = int(value)
        method_caller = methodcaller('setweight', value)
        for server in servers:
            try:
                method_caller(server)
                print("{} backend set weight to {} in {} backend".format(
                    server.name, value, server.backendname))
            except exceptions.CommandFailed as error:
                print("{} failed to change weight:{}".format(server.name,
                                                             error))
    except ValueError as error:
        sys.exit("{}".format(error))


def get_metric(servers, metric):
    if metric not in haproxy.SERVER_METRICS:
        sys.exit("{} no valid metric".format(metric))

    print("# backendname servername")
    for server in servers:
        print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                        server.metric(metric)))


def list_metrics():
    for metric in haproxy.SERVER_METRICS:
        print(metric)


def main():
    arguments = docopt(__doc__)
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

    servers = build_server_list(hap, arguments['NAME'], arguments['--backend'])

    if arguments['--list']:
        list_servers(servers)
    elif arguments['--status']:
        status(servers)
    elif arguments['--requests']:
        requests(servers)
    elif arguments['--sid']:
        sid(servers)
    elif arguments['--enable']:
        enable(servers)
    elif arguments['--disable']:
        disable(servers)
    elif arguments['--ready']:
        ready(servers)
    elif arguments['--drain']:
        drain(servers)
    elif arguments['--maintenance']:
        maintenance(servers)
    elif arguments['--process']:
        process(servers)
    elif arguments['--weight'] and arguments['VALUE']:
        weight(servers, arguments['VALUE'])
    elif arguments['--get-weight']:
        get_metric(servers, 'weight')
    elif arguments['METRIC']:
        get_metric(servers, arguments['METRIC'])
    elif arguments['--list-metrics']:
        list_metrics()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
