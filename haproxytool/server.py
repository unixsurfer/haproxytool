#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
# Created by: Pavlos Parissis <pavlos.parissis@booking.com>
#
"""Manage servers

Usage:
    haproxytool server [-D DIR | -h] (-r | -s | -e | -d | -R | -n | -t | -p | -W) [--pool=<name>...] [NAME...]
    haproxytool server [-D DIR | -h] -w VALUE [--pool=<name>...] [NAME...]
    haproxytool server [-D DIR | -h] (-l | -M)
    haproxytool server [-D DIR | -h] -m METRIC [--pool=<name>...] [NAME...]


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
    -s, --status              show status
    -m, --metric              show value of a metric
    -M, --list-metrics        show all metrics
    -l, --list                show all servers
    -w, --weight              change weight for server
    -W, --get-weight          show weight of server
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
    [default: /var/lib/haproxy]

"""
from docopt import docopt
from haproxyadmin import haproxy, exceptions
from operator import methodcaller


def build_server_list(hap, names=None, pools=None):
    servers = []
    if not names:
        if not pools:
            for server in hap.members():
                servers.append(server)
        else:
            for pool in pools:
                for server in hap.members(pool):
                    servers.append(server)
    else:
        if not pools:
            for name in names:
                try:
                    for server in hap.member(name):
                        servers.append(server)
                except ValueError:
                    print("{} was not found".format(name))
        else:
            for pool in pools:
                for name in names:
                    try:
                        for server in hap.member(name, pool):
                            servers.append(server)
                    except ValueError:
                        print("{} was not found".format(name))

    if not servers:
        exit(1)

    return servers


def list_servers(servers):
    print("# poolname servername")
    for server in servers:
        print("{:<30} {}".format(server.poolname, server.name))


def status(servers):
    print("# poolname servername")
    for server in servers:
        print("{:<30} {:<42} {}".format(server.poolname, server.name,
                                        server.status))


def requests(servers):
    print("# poolname servername")
    for server in servers:
        print("{:<30} {:<42} {}".format(server.poolname, server.name,
                                        server.requests))


def process(servers):
    print("# poolname servername")
    for server in servers:
        print("{:<30} {:<42} {}".format(server.poolname, server.name,
                                        server.process_nb))


def enable(servers):
    for server in servers:
        try:
            server.setstate(haproxy.STATE_ENABLE)
            print("{} enabled in {} pool".format(server.name, server.poolname))
        except exceptions.CommandFailed as error:
            print("{} failed to be enabled:{}".format(server.name, error))


def disable(servers):
    for server in servers:
        try:
            server.setstate(haproxy.STATE_DISABLE)
            print("{} disabled in {} pool".format(server.name, server.poolname))
        except exceptions.CommandFailed as error:
            print("{} failed to be disabled:{}".format(server.name, error))


def ready(servers):
    for server in servers:
        try:
            server.setstate(haproxy.STATE_READY)
            print("{} set to ready in {} pool".format(server.name,
                                                      server.poolname))
        except exceptions.CommandFailed as error:
            print("{} failed to set normal state:{}".format(server.name,
                                                            error))


def drain(servers):
    for server in servers:
        try:
            server.setstate(haproxy.STATE_DRAIN)
            print("{} set to drain in {} pool".format(server.name,
                                                      server.poolname))
        except exceptions.CommandFailed as error:
            print("{} failed to set in drain state:{}".format(server.name,
                                                              error))


def maintenance(servers):
    for server in servers:
        try:
            server.setstate(haproxy.STATE_READY)
            print("{} set to ready in {} pool".format(server.name,
                                                      server.poolname))
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
                print("{} pool set weight to {} in {} pool".format(
                    server.name, value, server.poolname))
            except exceptions.CommandFailed as error:
                print("{} failed to change weight:{}".format(server.name,
                                                             error))
    except ValueError as error:
        exit("{}".format(error))


def get_metric(servers, metric):
    if metric not in haproxy.SERVER_METRICS:
        exit("{} no valid metric".format(metric))

    print("# poolname servername")
    for server in servers:
        print("{:<30} {:<42} {}".format(server.poolname, server.name,
                                        server.metric(metric)))


def list_metrics():
    for metric in haproxy.SERVER_METRICS:
        print(metric)


def main():
    arguments = docopt(__doc__)
    hap = haproxy.HAProxy(socket_dir=arguments['--socket-dir'])

    servers = build_server_list(hap, arguments['NAME'], arguments['--pool'])

    if arguments['--list']:
        list_servers(servers)
    elif arguments['--status']:
        status(servers)
    elif arguments['--requests']:
        requests(servers)
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
