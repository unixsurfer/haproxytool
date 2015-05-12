# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File name: utils.py
#
# Creation date: 10-05-2015
#
# Created by: Pavlos Parissis <pavlos.parissis@booking.com>
#
import re
from operator import attrgetter


def sorted_nicely(l):
    """Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    # The element is an object for which I need to use its name as key value
    g = attrgetter('name')
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', g(key))]

    return sorted(l, key=alphanum_key)
