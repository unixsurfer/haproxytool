#!/usr/bin/env python
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
"""Manage backends

Usage:
    haproxytool backend [-D DIR | -F SOCKET] (-S | -r | -p | -s | -i) [NAME...]
    haproxytool backend [-D DIR | -F SOCKET] (-l | -M)
    haproxytool backend [-D DIR | -F SOCKET] -m METRIC [NAME...]

Arguments:
    DIR     Directory path with socket files
    SOCKET  Socket file
    METRIC  Name of a metric, use '-M' to get metric names

Options:
    -F SOCKET, --file SOCKET  socket file
    -h, --help                show this screen
    -i, --iid                 show proxy ID number
    -l, --show                show all backends
    -m, --metric              show value of a metric
    -M, --show-metrics        show all metrics
    -p, --process             show process number
    -r, --requests            show requests
    -s, --status              show status
    -S, --servers             show servers
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                              [default: /var/lib/haproxy]

"""
import sys
from docopt import docopt
from haproxyadmin import BACKEND_METRICS

from .utils import get_arg_option, haproxy_object


class BackendCommand():
    """Parse and run input from CLI

    Argument:
        hap (object): A haproxy.HAProxy object
        args (dict): A dictionary returned by docopt afte CLI is parsed
    """
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
        "report backend name"
        for backend in self.backends:
            print("{}".format(backend.name))

    def status(self):
        "report status of backends"
        for backend in self.backends:
            print("{} {}".format(backend.name, backend.status))

    def requests(self):
        "report traffic for backends"
        for backend in self.backends:
            print("{} {}".format(backend.name, backend.requests))

    def iid(self):
        "report proxy iid of backends"
        for backend in self.backends:
            print("{} {}".format(backend.name, backend.iid))

    def process(self):
        "report which HAProxy process manage which backends"
        for backend in self.backends:
            print("{} {}".format(backend.name, backend.process_nb))

    def servers(self):
        "report backend memberhips"
        for backend in self.backends:
            print("{}".format(backend.name))
            for server in backend.servers():
                print("{:<3} {}".format(' ', server.name))

    def metric(self):
        "report value of a metric"
        metric = self.args['METRIC']
        if metric not in BACKEND_METRICS:
            sys.exit("{} no valid metric".format(metric))

        for backend in self.backends:
            print("{} {}".format(backend.name, backend.metric(metric)))

    def showmetrics(self):
        "report all valid metrics for a backend"
        for metric in BACKEND_METRICS:
            print(metric)


def main():
    "Parse CLI"
    arguments = docopt(__doc__)
    hap = haproxy_object(arguments)

    cmd = BackendCommand(hap, arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
