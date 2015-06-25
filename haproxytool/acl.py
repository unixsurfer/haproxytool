#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
# Created by: Pavlos Parissis <pavlos.parissis@gmail.com>
#
"""Manage ACLs

Usage:
    haproxytool acl [-D DIR | -h] -l
    haproxytool acl [-D DIR | -h] (-c | -s) ACLID
    haproxytool acl [-D DIR | -h] (-g | -d) ACLID KEY
    haproxytool acl [-D DIR | -h] -A ACLID VALUE


Arguments:
    DIR     Directory path
    ACLID   ID of the acl or file returned by show acl
    KEY     ID of key
    VALUE   Value to set

Options:
    -h, --help                show this screen
    -A, --add                 add a <KEY> entry into the acl <ACLID>
    -s, --show                show acl
    -g, --get                 lookup the value of a key in the acl
    -c, --clear               clear all entries for a acl
    -l, --list                list all acl ids
    -d, --delete              delete all the acl entries from the acl <ACLID>
                              corresponding to the key <KEY>
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
                              [default: /var/lib/haproxy]

"""
import sys
from docopt import docopt
from haproxyadmin import haproxy
from haproxyadmin.exceptions import (CommandFailed,
                                     SocketApplicationError,
                                     SocketConnectionError,
                                     SocketPermissionError)
from .utils import get_arg_option


class ServerCommand(object):
    def __init__(self, hap, args):
        self.hap = hap
        self.args = args

    def list(self, aclid=None):
        try:
            for line in self.hap.show_acl(aclid=aclid):
                print(line)
        except CommandFailed as error:
            print(error)
            sys.exit(1)

    def show(self):
        aclid = self.args['ACLID']
        self.list(aclid)

    def clear(self):
        aclid = self.args['ACLID']
        try:
            if self.hap.clear_acl(aclid):
                print("all entries of acl were cleared successfully")
            else:
                print("failed to clear entries")
                sys.exit(1)
        except CommandFailed as error:
            print(error)
            sys.exit(1)

    def get(self):
        aclid = self.args['ACLID']
        key = self.args['KEY']
        try:
            print(self.hap.get_acl(aclid, key))
        except CommandFailed as error:
            print(error)
            sys.exit(1)

    def delele(self):
        aclid = self.args['ACLID']
        key = self.args['KEY']
        try:
            if self.hap.del_acl(aclid, key):
                print("key was deleted successfully")
            else:
                print("failed to delete key")
                sys.exit(1)
        except CommandFailed as error:
            print(error)
            sys.exit(1)

    def add(self):
        aclid = self.args['ACLID']
        key = self.args['KEY']
        value = self.args['VALUE']
        try:
            if self.hap.add_acl(aclid, key, value):
                print("key was added successfully")
            else:
                print("failed to add key in the acl")
                sys.exit(1)
        except CommandFailed as error:
            print(error)
            sys.exit(1)


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
    # if arguments['--list']:
    #     show_acl(hap, None)
    # elif arguments['--show']:
    #     show_acl(hap, arguments['ACLID'])
    # elif arguments['--set']:
    #     set_acl(hap, arguments['ACLID'], arguments['KEY'], arguments['VALUE'])
    # elif arguments['--add']:
    #     add_acl(hap, arguments['ACLID'], arguments['KEY'], arguments['VALUE'])
    # elif arguments['--clear']:
    #     clear_acl(hap, arguments['ACLID'])
    # elif arguments['--delete']:
    #     del_acl(hap, arguments['ACLID'], arguments['KEY'])
    # elif arguments['--get']:
    #     get_acl(hap, arguments['ACLID'], arguments['KEY'])

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
