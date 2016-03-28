#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
# pylint: disable=missing-docstring
#
# Created by: Pavlos Parissis <pavlos.parissis@gmail.com>
#
"""Manage servers

Usage:
    haproxytool server [-D DIR | -F SOCKET] (-r | -s | -e | -R | -p | -W | -i |
                       -c | -C | -S) [--backend=<name>...] [NAME...]
    haproxytool server [-D DIR | -F SOCKET] -w VALUE [--backend=<name>...]
                       [NAME...]
    haproxytool server [-D DIR | -F SOCKET] [-f ] (-d | -t | -n)
                       [--backend=<name>...] [NAME...]
    haproxytool server [-D DIR | -F SOCKET] (-l | -M)
    haproxytool server [-D DIR | -F SOCKET] -m METRIC [--backend=<name>...]
                       [NAME...]


Arguments:
    DIR     Directory path with socket files
    SOCKET  Socket file
    VALUE   Value to set
    METRIC  Name of a metric, use '-M' to get metric names

Options:
    -c, --show-check-code     show check code
    -C, --show-check-status   show check status
    -d, --disable             disable server
    -e, --enable              enable server
    -f, --force               force an operation
    -F SOCKET, --file SOCKET  socket file
    -h, --help                show this screen
    -i, --sid                 show server ID
    -l, --show                show all servers
    -m, --metric              show value of a metric
    -M, --show-metrics        show all metrics
    -n, --drain               drain server
    -p, --process             show process number
    -r, --requests            show requests
    -R, --ready               set server in normal mode
    -s, --status              show status
    -S, --show-last-status    show last check status
    -t, --maintenance         set server in maintenance mode
    -w, --weight              change weight for server
    -W, --get-weight          show weight of server
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                              [default: /var/lib/haproxy]

"""
import sys
from operator import methodcaller
from docopt import docopt
from haproxyadmin import (exceptions, SERVER_METRICS, STATE_ENABLE,
                          STATE_DISABLE, STATE_READY, STATE_DRAIN,
                          STATE_MAINT)
from haproxyadmin.exceptions import IncosistentData
from .utils import get_arg_option, abort_command, haproxy_object


class ServerCommand(object):
    """Parse and run input from CLI

    Argument:
        hap (object): A haproxy.HAProxy object
        args (dict): A dictionary returned by docopt afte CLI is parsed
    """
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

    def show(self):
        print("# backendname servername")
        for server in self.servers:
            print("{:<30} {}".format(server.backendname, server.name))

    def status(self):
        print("# backendname servername")
        for server in self.servers:
            try:
                status = server.status
            except IncosistentData as exc:
                status = exc.results
            print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                            status))

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
                server.setstate(STATE_ENABLE)
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
                server.setstate(STATE_DISABLE)
                print("{} disabled in {} backend".format(server.name,
                                                         server.backendname))
            except exceptions.CommandFailed as error:
                print("{} failed to be disabled:{}".format(server.name, error))

    def ready(self):
        for server in self.servers:
            try:
                server.setstate(STATE_READY)
                print("{} set to ready in {} backend".format(
                    server.name, server.backendname))
            except exceptions.CommandFailed as error:
                print("{} failed to set normal state:{}".format(server.name,
                                                                error))

    def drain(self):
        if abort_command('drain', 'servers', self.servers,
                         self.args['--force']):
            sys.exit('Aborted by user')

        for server in self.servers:
            try:
                server.setstate(STATE_DRAIN)
                print("{} set to drain in {} backend".format(
                    server.name, server.backendname))
            except exceptions.CommandFailed as error:
                print("{} failed to set in drain state:{}".format(server.name,
                                                                  error))

    def maintenance(self):
        if abort_command('maintenance', 'servers', self.servers,
                         self.args['--force']):
            sys.exit('Aborted by user')

        for server in self.servers:
            try:
                server.setstate(STATE_MAINT)
                print("{} set to maintenance in {} backend".format(
                    server.name, server.backendname))
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
        if metric not in SERVER_METRICS:
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

    def showmetrics(self):
        for metric in SERVER_METRICS:
            print(metric)

    def showcheckcode(self):
        print("# backendname servername")
        for server in self.servers:
            print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                            server.check_code))

    def showcheckstatus(self):
        print("# backendname servername")
        for server in self.servers:
            print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                            server.check_status))

    def showlaststatus(self):
        print("# backendname servername")
        for server in self.servers:
            print("{:<30} {:<42} {}".format(server.backendname, server.name,
                                            server.last_status))


def main():
    "Parse CLI"
    arguments = docopt(__doc__)
    hap = haproxy_object(arguments)

    cmd = ServerCommand(hap, arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
