.. haproxytool
.. README.rst

haproxytool
=================

    *A tool to manage `HAProxy <http://www.haproxy.org>`_ via stats socket.*

It uses `haproxyadmin <https://github.com/unixsurfer/haproxyadmin>`_
Python library to interact with HAProxy and run all commands.
One of the main feature is that can work with HAProxy in multi-process mode (nbproc > 1)

.. contents::

Release
-------

To make a release you should first create a signed tag, pbr will use this for the version number::

   git tag -s 0.0.9 -m 'bump release'
   git push --tags

Create the source distribution archive (the archive will be placed in the **dist** directory)::

   python setup.py sdist

Installation
------------

From Source::

   sudo python setup.py install

Build (source) RPMs::

   python setup.py clean --all; python setup.py bdist_rpm

Booking.com instructions::

   python setup.py clean --all
   python setup.py sdist

Build a source archive for manual installation::

   python setup.py sdist

Usage
-----
TOBEADDED

Licensing
---------

GPLv2

Contacts
--------

**Project website**: https://github.com/unixsurfer/haproxytool

**Author**: Palvos Parissis <pavlos.parissis@gmail.com>
