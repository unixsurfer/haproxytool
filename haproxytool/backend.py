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
    haproxytool backend [-D DIR | -h] (-S | -r | -p | -s | -i) [NAME...]
    haproxytool backend [-D DIR | -h] (-l | -M)
    haproxytool backend [-D DIR | -h] -m METRIC [NAME...]

Arguments:
    DIR     Directory path
    METRIC  Name of a metric, use '-M' to get metric names

Options:
    -h, --help                show this screen
    -S, --servers             show servers
    -r, --requests            show requests
    -p, --process             show process number
    -i, --iid                 show proxy ID number
    -s, --status              show status
    -m, --metric              show value of a metric
    -M, --list-metrics        show all metrics
    -l, --list                show all backends
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                              [default: /var/lib/haproxy]

"""
import sys
from docopt import docopt
from haproxyadmin import haproxy
from haproxyadmin.exceptions import (SocketApplicationError,
                                     SocketConnectionError,
                                     SocketPermissionError)


def build_backend_list(hap, names=None):
    backends = []
    if not names:
        for backend in hap.backends():
            backends.append(backend)
    else:
        for name in names:
            try:
                backends.append(hap.backend(name))
            except ValueError:
                print("{} was not found".format(name))

    if not backends:
        sys.exit(1)

    return backends


def list_backends(backends):
    for backend in backends:
        print("{}".format(backend.name))


def status(backends):
    for backend in backends:
        print("{} {}".format(backend.name, backend.status))


def requests(backends):
    for backend in backends:
        print("{} {}".format(backend.name, backend.requests))


def iid(backends):
    for backend in backends:
        print("{} {}".format(backend.name, backend.iid))


def process(backends):
    for backend in backends:
        print("{} {}".format(backend.name, backend.process_nb))


def servers(backends):
    for backend in backends:
        print("{}".format(backend.name))
        for server in backend.servers():
            print("{:<3} {}".format(' ', server.name))


def get_metric(backends, metric):
    """Retrieve the value of a metric.

    :param backends: A list of :class:`haproxy.Backend` objects
    :type backends: list
    :param metric: metric name
    :type metric: string
    :return: value of given metric
    """
    if metric not in haproxy.BACKEND_METRICS:
        sys.exit("{} no valid metric".format(metric))

    for backend in backends:
        print("{} {}".format(backend.name, backend.metric(metric)))


def list_metrics():
    """List all valid metric names."""
    for name in haproxy.SERVER_METRICS:
        print(name)


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

    # Build a list of backend objects
    backends = build_backend_list(hap, arguments['NAME'])

    if arguments['--list']:
        list_backends(backends)
    elif arguments['--status']:
        status(backends)
    elif arguments['--requests']:
        requests(backends)
    elif arguments['--iid']:
        iid(backends)
    elif arguments['METRIC']:
        get_metric(backends, arguments['METRIC'])
    elif arguments['--process']:
        process(backends)
    elif arguments['--list-metrics']:
        list_metrics()
    elif arguments['--servers']:
        servers(backends)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
