#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
#
"""Manage ACLs

Usage:
    haproxytool acl [(-D DIR | -F SOCK) | -h] -l
    haproxytool acl [(-D DIR | -F SOCK) | -h] (-c | -s) ACLID
    haproxytool acl [(-D DIR | -F SOCK) | -h] (-A | -g ) ACLID VALUE
    haproxytool acl [(-D DIR | -F SOCK) | -h] -d ACLID KEY


Arguments:
    DIR     Directory path
    SOCK    Socket file
    ACLID   ID of the acl or file returned by show acl
    VALUE   Value to set
    KEY     Key ID of ACL value/pattern

Options:
    -h, --help                show this screen
    -A, --add                 add a <KEY> entry into the acl <ACLID>
    -s, --show                show acl
    -g, --get                 lookup the value of a key in the acl
    -c, --clear               clear all entries for a acl
    -l, --list                list all acl ids
    -d, --delete              delete all the acl entries from the acl <ACLID>
                              corresponding to the key <KEY>
    -F SOCK, --socket=SOCK    use specific socket file
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


class AclCommand(object):
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
        value = self.args['VALUE']
        try:
            print(self.hap.get_acl(aclid, value))
        except CommandFailed as error:
            print(error)
            sys.exit(1)

    def delete(self):
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
        value = self.args['VALUE']
        try:
            if self.hap.add_acl(aclid, value):
                print("value was added successfully")
            else:
                print("failed to add value into the acl")
                sys.exit(1)
        except CommandFailed as error:
            print(error)
            sys.exit(1)


def main():
    arguments = docopt(__doc__)
    if (arguments['--socket']):
        try:
            hap = haproxy.HAProxy(socket_file=arguments['--socket'])
        except (SocketApplicationError,
                SocketConnectionError,
                SocketPermissionError) as error:
            print(error, error.socket_file)
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
            print(error, error.socket_file)
            sys.exit(1)
        except ValueError as error:
            print(error)
            sys.exit(1)

    cmd = AclCommand(hap, arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
