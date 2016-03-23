#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
# Created by: Pavlos Parissis <pavlos.parissis@gmail.com>
#
"""Manage backends

Usage:
    haproxytool backend [(-D DIR | -F SOCK)] (-S | -r | -p | -s | -i) [NAME...]
    haproxytool backend [(-D DIR | -F SOCK)] (-l | -M)
    haproxytool backend [(-D DIR | -F SOCK)] -m METRIC [NAME...]

Arguments:
    DIR     Directory path
    SOCK    Socket file
    METRIC  Name of a metric, use '-M' to get metric names

Options:
    -h, --help                show this screen
    -i, --iid                 show proxy ID number
    -l, --show                show all backends
    -m, --metric              show value of a metric
    -M, --show-metrics        show all metrics
    -p, --process             show process number
    -r, --requests            show requests
    -s, --status              show status
    -S, --servers             show servers
    -F SOCK, --socket=SOCK    use specific socket file
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                              [default: /var/lib/haproxy]

"""
import sys
from docopt import docopt
from haproxyadmin import haproxy, BACKEND_METRICS
from haproxyadmin.exceptions import (SocketApplicationError,
                                     SocketConnectionError,
                                     SocketPermissionError)
from .utils import get_arg_option


class BackendCommand(object):
    def __init__(self, hap, args):
        self.hap = hap
        self.args = args
        self.backends = self.build_backend_list(args['NAME'])

    def build_backend_list(self, names=None):
        backends = []
        if not names:
            for backend in self.hap.backends():
                backends.append(backend)
        else:
            for name in names:
                try:
                    backends.append(self.hap.backend(name))
                except ValueError:
                    print("{} was not found".format(name))

        return backends

    def show(self):
        for backend in self.backends:
            print("{}".format(backend.name))

    def status(self):
        for backend in self.backends:
            print("{} {}".format(backend.name, backend.status))

    def requests(self):
        for backend in self.backends:
            print("{} {}".format(backend.name, backend.requests))

    def iid(self):
        for backend in self.backends:
            print("{} {}".format(backend.name, backend.iid))

    def process(self):
        for backend in self.backends:
            print("{} {}".format(backend.name, backend.process_nb))

    def servers(self):
        for backend in self.backends:
            print("{}".format(backend.name))
            for server in backend.servers():
                print("{:<3} {}".format(' ', server.name))

    def metric(self):
        metric = self.args['METRIC']
        if metric not in BACKEND_METRICS:
            sys.exit("{} no valid metric".format(metric))

        for backend in self.backends:
            print("{} {}".format(backend.name, backend.metric(metric)))

    def showmetrics(self):
        for metric in BACKEND_METRICS:
            print(metric)


def main():
    arguments = docopt(__doc__)

    if (arguments['--socket']):
        try:
            hap = haproxy.HAProxy(socket_file=arguments['--socket'])
        except (SocketApplicationError,
                SocketConnectionError,
                SocketPermissionError) as error:
            print(error)
            sys.exit(1)
        except ValueError as error:
            print(error)
            sys.exit(1)
    else:
        try:
            hap = haproxy.HAProxy(socket_dir=arguments['--socket-dir'])
        except (SocketApplicationError,
                SocketConnectionError,
                SocketPermissionError) as error:
            print(error)
            sys.exit(1)
        except ValueError as error:
            print(error)
            sys.exit(1)

    cmd = BackendCommand(hap, arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
