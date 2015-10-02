# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Created by: Pavlos Parissis <pavlos.parissis@gmail.com>
#
from six.moves import input


def get_arg_option(args):
    for key, value in args.items():
        if (key != '--force' and key.startswith('--') and
                isinstance(value, bool) and value):
            return key.replace('-', '')


def read_user(msg):
    """Read user input.

    :param msg: A message to prompt
    :type msg: ``str``
    :return: ``True`` if user gives 'y' otherwhise False.
    :rtype: ``bool``
    """
    user_input = input("{msg} y/n?: ".format(msg=msg))
    if user_input == 'y':
        return True
    else:
        return False


def abort_command(command, object_type, objects, force):
    nbobjects = len(objects)
    msg = "Are you sure we want to {cmd} {n} {obg_type}".format(
        cmd=command, n=nbobjects, obg_type=object_type)
    if not force and nbobjects > 1:
        if not read_user(msg):
            return True

    return False
