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
    haproxytool map [-D DIR | -h] -l
    haproxytool map [-D DIR | -h] (-s | -c ) MAPID
    haproxytool map [-D DIR | -h] -g MAPID KEY
    haproxytool map [-D DIR | -h] (-S | -A) MAPID KEY VALUE
    haproxytool map [-D DIR | -h] -d MAPID KEY


Arguments:
    DIR     Directory path
    MAPID   ID of the map or file returned by show map
    KEY     ID of key
    VALUE   Value to set

Options:
    -h, --help                show this screen
    -A, --add                 add an <KEY> entry into the map <MAPID>
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
from docopt import docopt
from haproxyadmin import haproxy
from haproxyadmin.exceptions import (CommandFailed,
                                     SocketApplicationError,
                                     SocketConnectionError,
                                     SocketPermissionError)

def show_map(hap, mapid):

    try:
        for line in hap.show_map(mapid=mapid):
            print(line)
    except CommandFailed as error:
        print(error)
        exit(1)

def clear_map(hap, mapid):
    try:
        if hap.clear_map(mapid):
            print("all entries of map were cleared successfully")
        else:
            print("failed to clear entries")
            exit(1)
    except CommandFailed as error:
        print(error)
        exit(1)

def get_map(hap, mapid, key):
    try:
        print(hap.get_map(mapid, key))
    except CommandFailed as error:
        print(error)
        exit(1)

def del_map(hap, mapid, key):
    try:
        if hap.del_map(mapid, key):
            print("key was deleted successfully")
        else:
            print("failed to delete key")
            exit(1)
    except CommandFailed as error:
        print(error)
        exit(1)

def add_map(hap, mapid, key, value):
    try:
        if hap.add_map(mapid, key, value):
            print("key was added successfully")
        else:
            print("failed to add key in the map")
            exit(1)
    except CommandFailed as error:
        print(error)
        exit(1)

def set_map(hap, mapid, key, value):
    try:
        if hap.set_map(mapid, key, value):
            print("value was set successfully")
        else:
            print("failed to set value")
            exit(1)
    except CommandFailed as error:
        print(error)
        exit(1)

def main():
    arguments = docopt(__doc__)
    try:
        hap = haproxy.HAProxy(socket_dir=arguments['--socket-dir'])
    except (SocketApplicationError,
            SocketConnectionError,
            SocketPermissionError) as error:
        print(error, error.socket_file)
        exit(1)

    print(arguments)
    if arguments['--list']:
        show_map(hap, None)
    elif arguments['--show']:
        show_map(hap, arguments['MAPID'])
    elif arguments['--set']:
        set_map(hap, arguments['MAPID'], arguments['KEY'], arguments['VALUE'])
    elif arguments['--add']:
        add_map(hap, arguments['MAPID'], arguments['KEY'], arguments['VALUE'])
    elif arguments['--clear']:
        clear_map(hap, arguments['MAPID'])
    elif arguments['--delete']:
        del_map(hap, arguments['MAPID'], arguments['KEY'])
    elif arguments['--get']:
        get_map(hap, arguments['MAPID'], arguments['KEY'])

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
