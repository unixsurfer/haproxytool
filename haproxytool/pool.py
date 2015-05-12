#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
# File name: haproxy_pool.py
#
# Creation date: 09-05-2015
#
# Created by: Pavlos Parissis <pavlos.parissis@booking.com>
#
"""Manage pools

Usage:
    haproxytool pool [-D DIR | -h] (-S | -r | -p | -s) [NAME...]
    haproxytool pool [-D DIR | -h] --list
    haproxytool pool [-D DIR | -h] (-l | -M)
    haproxytool pool [-D DIR | -h] -m METRIC NAME...

Arguments:
    DIR     Directory path
    METRIC   Name of a metric, use '-M' to get metric names

Options:
    -h, --help                show this screen
    -S, --servers             show members
    -r, --requests            show requests
    -p, --process             show process number
    -s, --status              show status
    -m, --metric              show value of a metric
    -M, --list-metrics        show all metrics
    -l, --list                show all pools
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
    [default: /var/lib/haproxy]

"""
from docopt import docopt
from haproxyadmin import haproxy


def build_pool_list(hap, names=None):
    pools = []
    if not names:
        for pool in hap.pools():
            pools.append(pool)
    else:
        for name in names:
            try:
                pools.append(hap.pool(name))
            except ValueError:
                print("{} was not found".format(name))

    if not pools:
        exit("No pool was found")

    return pools


def list_pools(hap):
    pools = build_pool_list(hap)
    for pool in pools:
        print("{}".format(pool.name))


def status(pools):
    for pool in pools:
        print("{} {}".format(pool.name, pool.status))


def requests(pools):
    for pool in pools:
        print("{} {}".format(pool.name, pool.requests))


def process(pools):
    for pool in pools:
        print("{} {}".format(pool.name, pool.process_nb))


def servers(pools):
    for pool in pools:
        print("{}".format(pool.name))
        for server in pool.members():
            print("{:<3} {}".format(' ', server.name))


def get_metric(pools, metric):
    """Retrieve the value of a metric.

    :param pools: A list of :class:`haproxy.Pool` objects
    :type pools: list
    :param metric: metric name
    :type metric: string
    :return: value of given metric
    """
    if metric not in haproxy.POOL_METRICS:
        exit("{} no valid metric".format(metric))

    for pool in pools:
        print("{} {}".format(pool.name, pool.metric(metric)))


def list_metrics():
    """List all valid metric names."""
    for name in haproxy.SERVER_METRICS:
        print(name)


def main():
    arguments = docopt(__doc__)
    hap = haproxy.HAProxy(socket_dir=arguments['--socket-dir'])

    # Build a list of pool objects
    if arguments['NAME']:
        pools = build_pool_list(hap, arguments['NAME'])
    else:
        pools = build_pool_list(hap)

    if arguments['--list']:
        list_pools(hap)
    elif arguments['--status']:
        status(pools)
    elif arguments['--requests']:
        requests(pools)
    elif arguments['METRIC']:
        get_metric(pools, arguments['METRIC'])
    elif arguments['--process']:
        process(pools)
    elif arguments['--list-metrics']:
        list_metrics()
    elif arguments['--servers']:
        servers(pools)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
