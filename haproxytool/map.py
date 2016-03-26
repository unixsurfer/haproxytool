#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
# Created by: Pavlos Parissis <pavlos.parissis@gmail.com>
#
"""Manage MAPs

Usage:
    haproxytool map [-D DIR | -F SOCKET] -l
    haproxytool map [-D DIR | -F SOCKET] (-s | -c ) MAPID
    haproxytool map [-D DIR | -F SOCKET] -g MAPID KEY
    haproxytool map [-D DIR | -F SOCKET] (-S | -A) MAPID KEY VALUE
    haproxytool map [-D DIR | -F SOCKET] -d MAPID KEY


Arguments:
    DIR     Directory path with socket files
    MAPID   ID of the map or file returned by show map
    KEY     ID of key
    SOCKET  Socket file
    VALUE   Value to set

Options:
    -A, --add                 add a <KEY> entry into the map <MAPID>
    -F SOCKET, --file SOCKET  socket file
    -h, --help                show this screen
    -s, --show                show map
    -g, --get                 lookup the value of a key in the map
    -c, --clear               clear all entries for a map
    -l, --list                list all map ids
    -S, --set                 set a new value for a key in a map
    -d, --delete              delete all the map entries from the map <MAPID>
                              corresponding to the key <KEY>
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                              [default: /var/lib/haproxy]

"""
import sys
from docopt import docopt
from haproxyadmin.exceptions import CommandFailed

from .utils import get_arg_option, haproxy_object


class MapCommand(object):
    def __init__(self, hap, args):
        self.hap = hap
        self.args = args

    def list(self, mapid=None):
        try:
            for line in self.hap.show_map(mapid=mapid):
                print(line)
        except (CommandFailed, ValueError) as error:
            print(error)
            sys.exit(1)

    def show(self):
        mapid = self.args['MAPID']
        self.list(mapid)

    def clear(self):
        try:
            if self.hap.clear_map(self.args['MAPID']):
                print("all entries of map were cleared successfully")
            else:
                print("failed to clear entries")
                sys.exit(1)
        except CommandFailed as error:
            print(error)
            sys.exit(1)

    def get(self):
        try:
            print(self.hap.get_map(self.args['MAPID'], self.args['KEY']))
        except CommandFailed as error:
            print(error)
            sys.exit(1)

    def delete(self):
        try:
            if self.hap.del_map(self.args['MAPID'], self.args['KEY']):
                print("key was deleted successfully")
            else:
                print("failed to delete key")
                sys.exit(1)
        except CommandFailed as error:
            print(error)
            sys.exit(1)

    def add(self):
        try:
            if self.hap.add_map(self.args['MAPID'],
                                self.args['KEY'],
                                self.args['VALUE']):
                print("key was added successfully")
            else:
                print("failed to add key in the map")
                sys.exit(1)
        except CommandFailed as error:
            print(error)
            sys.exit(1)

    def set(self):
        try:
            if self.hap.set_map(self.args['MAPID'],
                                self.args['KEY'],
                                self.args['VALUE']):
                print("value was set successfully")
            else:
                print("failed to set value")
                sys.exit(1)
        except CommandFailed as error:
            print(error)
            sys.exit(1)


def main():
    arguments = docopt(__doc__)
    hap = haproxy_object(arguments)

    cmd = MapCommand(hap, arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
