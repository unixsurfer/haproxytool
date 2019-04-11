#!/usr/bin/env python
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
#
"""Manage ACLs

Usage:
    haproxytool acl [-D DIR | -F SOCKET] -l
    haproxytool acl [-D DIR | -F SOCKET] (-c | -s) ACLID
    haproxytool acl [-D DIR | -F SOCKET] (-A | -g ) ACLID VALUE
    haproxytool acl [-D DIR | -F SOCKET] -d ACLID KEY


Arguments:
    DIR     Directory path with socket files
    ACLID   ID of the acl or file returned by show acl
    SOCKET  Socket file
    VALUE   Value to set
    KEY     Key ID of ACL value/pattern

Options:
    -h, --help                show this screen
    -A, --add                 add a <KEY> entry into the acl <ACLID>
    -F SOCKET, --file SOCKET  socket file
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
from haproxyadmin.exceptions import CommandFailed
from .utils import get_arg_option, haproxy_object


class AclCommand(object):
    def __init__(self, hap, args):
        self.hap = hap
        self.args = args

    def list(self, aclid=None):
        try:
            acl_entries = self.hap.show_acl(aclid=aclid)
        except (CommandFailed, ValueError) as error:
            sys.exit(error)
        else:
            if not acl_entries:
                print("acl doesn't have any entries")
            else:
                for entry in acl_entries:
                    print(entry)

    def show(self):
        aclid = self.args['ACLID']
        self.list(aclid)

    def clear(self):
        aclid = self.args['ACLID']
        try:
            if self.hap.clear_acl(aclid):
                print("all entries of acl were cleared successfully")
            else:
                sys.exit("failed to clear entries")
        except (CommandFailed, ValueError) as error:
            sys.exit(error)

    def get(self):
        aclid = self.args['ACLID']
        value = self.args['VALUE']
        try:
            print(self.hap.get_acl(aclid, value))
        except (CommandFailed, ValueError) as error:
            sys.exit(error)

    def delete(self):
        aclid = self.args['ACLID']
        key = self.args['KEY']
        try:
            if self.hap.del_acl(aclid, key):
                print("key was deleted successfully")
            else:
                sys.exit("failed to delete key")
        except (CommandFailed, ValueError) as error:
            sys.exit(error)

    def add(self):
        aclid = self.args['ACLID']
        value = self.args['VALUE']
        try:
            if self.hap.add_acl(aclid, value):
                print("value was added successfully")
            else:
                sys.exit("failed to add value into the acl")
        except (CommandFailed, ValueError) as error:
            sys.exit(error)


def main():
    arguments = docopt(__doc__)
    hap = haproxy_object(arguments)

    cmd = AclCommand(hap, arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
