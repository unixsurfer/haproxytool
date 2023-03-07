#!/usr/bin/env python
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
# pylint: disable=missing-docstring
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


class MapCommand():
    def __init__(self, hap, args):
        self.hap = hap
        self.args = args

    def list(self, mapid=None):
        try:
            map_entries = self.hap.show_map(mapid=mapid)
        except (CommandFailed, ValueError) as error:
            sys.exit(error)
        else:
            if not map_entries:
                print("map doesn't have any entries")
            else:
                for entry in map_entries:
                    print(entry)

    def show(self):
        mapid = self.args['MAPID']
        self.list(mapid)

    def clear(self):
        try:
            if self.hap.clear_map(self.args['MAPID']):
                print("all entries of map were cleared successfully")
            else:
                sys.exit("failed to clear entries")
        except (CommandFailed, ValueError) as error:
            sys.exit(error)

    def get(self):
        try:
            print(self.hap.get_map(self.args['MAPID'], self.args['KEY']))
        except (CommandFailed, ValueError) as error:
            sys.exit(error)

    def delete(self):
        try:
            if self.hap.del_map(self.args['MAPID'], self.args['KEY']):
                print("key was deleted successfully")
            else:
                sys.exit("failed to delete key")
        except (CommandFailed, ValueError) as error:
            sys.exit(error)

    def add(self):
        try:
            if self.hap.add_map(self.args['MAPID'],
                                self.args['KEY'],
                                self.args['VALUE']):
                print("key was added successfully")
            else:
                sys.exit("failed to add key in the map")
        except (CommandFailed, ValueError) as error:
            sys.exit(error)

    def set(self):
        try:
            if self.hap.set_map(self.args['MAPID'],
                                self.args['KEY'],
                                self.args['VALUE']):
                print("value was set successfully")
            else:
                sys.exit("failed to set value")
        except (CommandFailed, ValueError) as error:
            sys.exit(error)


def main():
    arguments = docopt(__doc__)
    hap = haproxy_object(arguments)

    cmd = MapCommand(hap, arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
