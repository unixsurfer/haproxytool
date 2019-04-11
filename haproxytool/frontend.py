#!/usr/bin/env python
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
"""Manage frontends

Usage:
    haproxytool frontend [-D DIR -F SOCKET] (-c | -r | -s | -o | -e | -p | -i)
                         [NAME...]
    haproxytool frontend [-D DIR -F SOCKET] -w OPTION VALUE [NAME...]
    haproxytool frontend [-D DIR -F SOCKET] [-f ] (-d | -t) [NAME...]
    haproxytool frontend [-D DIR -F SOCKET] (-l | -M)
    haproxytool frontend [-D DIR -F SOCKET] -m METRIC [NAME...]

Arguments:
    DIR     Directory path with socket files
    SOCKET  Socket file
    VALUE   Value to set
    OPTION  Setting name
    METRIC  Name of a metric, use '-M' to get metric names

Options:
    -c, --showmaxconn         show max sessions
    -d, --disable             disable frontend
    -e, --enable              enable frontend
    -f, --force               force an operation
    -F SOCKET, --file SOCKET  socket file
    -h, --help                show this screen
    -i, --iid                 show proxy ID number
    -l, --show                show all frontends
    -m, --metric              show value of a metric
    -M, --show-metrics        show all metrics
    -o, --options             show value of options that can be changed with
                              '-w' option
    -p, --process             show process number
    -r, --requests            show requests
    -s, --status              show status
    -t, --shutdown            shutdown frontend
    -w, --write               change a frontend option
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                              [default: /var/lib/haproxy]

"""
import sys
from operator import methodcaller
from docopt import docopt
from haproxyadmin import FRONTEND_METRICS
from haproxyadmin.exceptions import CommandFailed

from .utils import get_arg_option, abort_command, haproxy_object


class FrontendCommand():
    def __init__(self, hap, args):
        self.hap = hap
        self.args = args
        self.frontends = self.build_frontend_list(args['NAME'])

    def build_frontend_list(self, names=None):
        frontends = []
        if not names:
            for frontend in self.hap.frontends():
                frontends.append(frontend)
        else:
            for name in names:
                try:
                    frontends.append(self.hap.frontend(name))
                except ValueError:
                    print("{} was not found".format(name))

        return frontends

    def show(self):
        for frontend in self.frontends:
            print("{}".format(frontend.name))

    def status(self):
        for frontend in self.frontends:
            print("{} {}".format(frontend.name, frontend.status))

    def requests(self):
        for frontend in self.frontends:
            print("{} {}".format(frontend.name, frontend.requests))

    def iid(self):
        for frontend in self.frontends:
            print("{} {}".format(frontend.name, frontend.iid))

    def process(self):
        for frontend in self.frontends:
            print("{} {}".format(frontend.name, frontend.process_nb))

    def options(self):
        for frontend in self.frontends:
            print("{} maxconn={}".format(frontend.name, frontend.maxconn))

    def enable(self):
        for frontend in self.frontends:
            try:
                frontend.enable()
                print("{} enabled".format(frontend.name))
            except CommandFailed as error:
                print("{} failed to be enabled:{}".format(frontend.name,
                                                          error))

    def disable(self):
        if abort_command('disable', 'frontends', self.frontends,
                         self.args['--force']):
            sys.exit('Aborted by user')

        for frontend in self.frontends:
            try:
                frontend.disable()
                print("{} disabled".format(frontend.name))
            except CommandFailed as error:
                print("{} failed to be disabled:{}".format(frontend.name,
                                                           error))

    def shutdown(self):
        if abort_command('shutdown', 'frontends', self.frontends,
                         self.args['--force']):
            sys.exit('Aborted by user')

        for frontend in self.frontends:
            try:
                frontend.shutdown()
                print("{} shutdown".format(frontend.name))
            except CommandFailed as error:
                print("{} failed to be shutdown:{}".format(frontend.name,
                                                           error))

    def write(self):
        setting = self.args['OPTION']
        value = self.args['VALUE']
        try:
            value = int(value)
            call_method = methodcaller('setmaxconn', value, die=False)
            for frontend in self.frontends:
                if call_method(frontend):
                    print("{} set {} to {}".format(frontend.name,
                                                   setting,
                                                   value))
                else:
                    print("{} failed to set maxconn on {}".format(frontend.name,
                                                                  value))
        except ValueError:
            sys.exit("You need to pass a number, got {}".format(value))

    def metric(self):
        metric = self.args['METRIC']
        if metric not in FRONTEND_METRICS:
            sys.exit("{} no valid metric".format(metric))

        for frontend in self.frontends:
            print("{} {}".format(frontend.name, frontend.metric(metric)))

    def showmetrics(self):
        for metric in FRONTEND_METRICS:
            print(metric)

    def showmaxconn(self):
        for frontend in self.frontends:
            print("{n} {s}".format(n=frontend.name, s=frontend.maxconn))


def main():
    arguments = docopt(__doc__)
    hap = haproxy_object(arguments)

    cmd = FrontendCommand(hap, arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
