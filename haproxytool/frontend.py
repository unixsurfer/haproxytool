#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
#
# Created by: Pavlos Parissis <pavlos.parissis@gmail.com>
#
"""Manage frontends

Usage:
    haproxytool frontend [-D DIR | -h] (-r | -s | -o | -e | -d | -t | -p | -i) [NAME...]
    haproxytool frontend [-D DIR | -h] -w OPTION VALUE [NAME...]
    haproxytool frontend [-D DIR | -h] (-l | -M)
    haproxytool frontend [-D DIR | -h] -m METRIC [NAME...]

Arguments:
    DIR     Directory path
    VALUE   Value to set
    OPTION  Setting name
    METRIC  Name of a metric, use '-M' to get metric names

Options:
    -h, --help                show this screen
    -e, --enable              enable frontend
    -d, --disable             disable frontend
    -t, --shutdown            shutdown frontend
    -r, --requests            show requests
    -p, --process             show process number
    -i, --iid                 show proxy ID number
    -s, --status              show status
    -o, --options             show value of options that can be changed with '-w'
    -m, --metric              show value of a metric
    -M, --list-metrics        show all metrics
    -l, --list                show all frontends
    -w, --write               change a frontend option
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
    [default: /var/lib/haproxy]

"""
from docopt import docopt
from haproxyadmin import haproxy, exceptions
from operator import methodcaller
from haproxyadmin.exceptions import (SocketApplicationError,
                                     SocketConnectionError,
                                     SocketPermissionError)


def build_frontend_list(hap, names=None):
    frontends = []
    if not names:
        for frontend in hap.frontends():
            frontends.append(frontend)
    else:
        for name in names:
            try:
                frontends.append(hap.frontend(name))
            except ValueError:
                print("{} was not found".format(name))

    if not frontends:
        exit(1)

    return frontends


def list_frontends(frontends):
    for frontend in frontends:
        print("{}".format(frontend.name))


def status(frontends):
    for frontend in frontends:
        print("{} {}".format(frontend.name, frontend.status))


def requests(frontends):
    for frontend in frontends:
        print("{} {}".format(frontend.name, frontend.requests))


def iid(frontends):
    for frontend in frontends:
        print("{} {}".format(frontend.name, frontend.iid))


def process(frontends):
    for frontend in frontends:
        print("{} {}".format(frontend.name, frontend.process_nb))


def options(frontends):
    for frontend in frontends:
        print("{} maxconn={}".format(frontend.name, frontend.maxconn))


def enable(frontends):
    for frontend in frontends:
        try:
            frontend.enable()
            print("{} enabled".format(frontend.name))
        except exceptions.CommandFailed as error:
            print("{} failed to be enabled:{}".format(frontend.name, error))


def disable(frontends):
    for frontend in frontends:
        try:
            frontend.disable()
            print("{} disabled".format(frontend.name))
        except exceptions.CommandFailed as error:
            print("{} failed to be disabled:{}".format(frontend.name, error))


def shutdown(frontends):
    for frontend in frontends:
        try:
            frontend.shutdown()
            print("{} shutdown".format(frontend.name))
        except exceptions.CommandFailed as error:
            print("{} failed to be shutdown:{}".format(frontend.name, error))


def set_option(frontends, setting, value):
    try:
        value = int(value)
        call_method = methodcaller('setmaxconn', value, die=False)
        for frontend in frontends:
            if call_method(frontend):
                print("{} set {} to {}".format(frontend.name, setting, value))
            else:
                print("{} failed to set maxconn to {}".format(frontend.name,
                                                              value))
    except ValueError:
        exit("You need to pass a number, got {}".format(value))


def get_metric(frontends, metric):
    if metric not in haproxy.FRONTEND_METRICS:
        exit("{} no valid metric".format(metric))

    for frontend in frontends:
        print("{} {}".format(frontend.name, frontend.metric(metric)))


def list_metrics():
    for metric in haproxy.FRONTEND_METRICS:
        print(metric)


def main():
    arguments = docopt(__doc__)

    try:
        hap = haproxy.HAProxy(socket_dir=arguments['--socket-dir'])
    except (SocketApplicationError,
            SocketConnectionError,
            SocketPermissionError) as error:
        print(error, error.socket_file)
        exit(1)
    frontends = build_frontend_list(hap, arguments['NAME'])

    if arguments['--list']:
        list_frontends(frontends)
    elif arguments['--status']:
        status(frontends)
    elif arguments['--requests']:
        requests(frontends)
    elif arguments['--iid']:
        iid(frontends)
    elif arguments['--options']:
        options(frontends)
    elif arguments['--enable']:
        enable(frontends)
    elif arguments['--disable']:
        disable(frontends)
    elif arguments['--process']:
        process(frontends)
    elif arguments['--shutdown']:
        shutdown(frontends)
    elif arguments['OPTION'] and arguments['VALUE']:
        set_option(frontends, arguments['OPTION'], arguments['VALUE'])
    elif arguments['METRIC']:
        get_metric(frontends, arguments['METRIC'])
    elif arguments['--list-metrics']:
        list_metrics()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
