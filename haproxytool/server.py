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
    haproxytool server [-D DIR ] (-r | -s | -e | -R | -p | -W | -i) [--backend=<name>...] [NAME...]
    haproxytool server [-D DIR ] -w VALUE [--backend=<name>...] [NAME...]
    haproxytool server [-D DIR -f ] (-d | -t | -n) [--backend=<name>...] [NAME...]
    haproxytool server [-D DIR ] (-l | -M)
    haproxytool server [-D DIR ] -m METRIC [--backend=<name>...] [NAME...]


Arguments:
    DIR     Directory path
    VALUE   Value to set
    METRIC  Name of a metric, use '-M' to get metric names

Options:
    -d, --disable             disable server
    -e, --enable              enable server
    -f, --force               force an operation
    -h, --help                show this screen
    -i, --sid                 show server ID
    -l, --list                show all servers
    -m, --metric              show value of a metric
    -M, --list-metrics        show all metrics
    -n, --drain               drain server
    -p, --process             show process number
    -r, --requests            show requests
    -R, --ready               set server in normal mode
    -s, --status              show status
    -t, --maintenance         set server in maintenance mode
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
from .utils import get_arg_option, abort_command


class ServerCommand(object):
    def __init__(self, hap, args):
        self.hap = hap
        self.args = args
        self.servers = self.build_server_list(
            args['NAME'],
            args['--backend'])

    def build_server_list(self, names=None, backends=None):
        servers = []
        if not names:
            if not backends:
                for server in self.hap.servers():
                    servers.append(server)
            else:
                for backend in backends:
                    for server in self.hap.servers(backend):
                        servers.append(server)
        else:
            if not backends:
                for name in names:
                    try:
                        for server in self.hap.server(name):
                            servers.append(server)
                    except ValueError:
                        print("{} was not found".format(name))
            else:
                for backend in backends:
                    for name in names:
                        try:
                            for server in self.hap.server(name, backend):
                                servers.append(server)
                        except ValueError:
                            print("{} was not found".format(name))

        return servers

    def list(self):
        print("# backendname servername")
        for server in self.servers:
            print("{:<30} {}".format(server.backendname, server.name))

    def status(self):
        print("# backendname servername")
        for server in self.servers:
            print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                            server.status))

    def requests(self):
        print("# backendname servername")
        for server in self.servers:
            print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                            server.requests))

    def sid(self):
        print("# backendname servername")
        for server in self.servers:
            print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                            server.sid))

    def process(self):
        print("# backendname servername")
        for server in self.servers:
            print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                            server.process_nb))

    def enable(self):
        for server in self.servers:
            try:
                server.setstate(haproxy.STATE_ENABLE)
                print("{} enabled in {} backend".format(server.name,
                                                        server.backendname))
            except exceptions.CommandFailed as error:
                print("{} failed to be enabled:{}".format(server.name, error))

    def disable(self):
        if abort_command('disable', 'servers', self.servers,
                         self.args['--force']):
            sys.exit('Aborted by user')

        for server in self.servers:
            try:
                server.setstate(haproxy.STATE_DISABLE)
                print("{} disabled in {} backend".format(server.name,
                                                         server.backendname))
            except exceptions.CommandFailed as error:
                print("{} failed to be disabled:{}".format(server.name, error))

    def ready(self):
        for server in self.servers:
            try:
                server.setstate(haproxy.STATE_READY)
                print("{} set to ready in {} backend".format(
                    server.name, server.backendname)
                )
            except exceptions.CommandFailed as error:
                print("{} failed to set normal state:{}".format(server.name,
                                                                error))

    def drain(self):
        if abort_command('drain', 'servers', self.servers,
                         self.args['--force']):
            sys.exit('Aborted by user')

        for server in self.servers:
            try:
                server.setstate(haproxy.STATE_DRAIN)
                print("{} set to drain in {} backend".format(
                    server.name, server.backendname)
                )
            except exceptions.CommandFailed as error:
                print("{} failed to set in drain state:{}".format(server.name,
                                                                  error))

    def maintenance(self):
        if abort_command('maintenance', 'servers', self.servers,
                         self.args['--force']):
            sys.exit('Aborted by user')

        for server in self.servers:
            try:
                server.setstate(haproxy.STATE_MAINT)
                print("{} set to maintenance in {} backend".format(
                    server.name, server.backendname)
                )
            except exceptions.CommandFailed as error:
                print("{} failed to set to maintenance state:{}".format(
                    server.name, error))

    def weight(self):
        value = self.args['VALUE']
        try:
            value = int(value)
            method_caller = methodcaller('setweight', value)
            for server in self.servers:
                try:
                    method_caller(server)
                    print("{} backend set weight to {} in {} backend".format(
                        server.name, value, server.backendname))
                except exceptions.CommandFailed as error:
                    print("{} failed to change weight:{}".format(server.name,
                                                                 error))
        except ValueError as error:
            sys.exit("{}".format(error))

    def metric(self):
        metric = self.args['METRIC']
        if metric not in haproxy.SERVER_METRICS:
            sys.exit("{} no valid metric".format(metric))

        print("# backendname servername")
        for server in self.servers:
            print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                            server.metric(metric)))

    def getweight(self):
        print("# backendname servername")
        for server in self.servers:
            print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                            server.weight))

    def listmetrics(self):
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

    cmd = ServerCommand(hap, arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
